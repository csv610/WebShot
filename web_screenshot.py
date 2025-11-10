"""
WebScreenShot - A tool for capturing full-page screenshots of websites using Playwright.

Features:
- URL validation with blank image fallback
- Configurable timeouts and delays
- Custom viewport support with auto-adjustment
- Reusable browser instance for multiple screenshots
- Configuration file support (YAML)
- Handles lazy-loaded images
"""

# Standard library imports
import logging
import os
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional
from urllib.parse import urlparse

# Third-party imports
import yaml
from PIL import Image
from playwright.sync_api import Browser, Page, sync_playwright


@dataclass
class ScreenShotConfig:
    """Configuration dataclass for WebScreenShot settings."""

    # Timeout settings (in milliseconds)
    navigation_timeout: int = 60000
    action_timeout: int = 60000
    final_wait: int = 5000

    # Scroll settings (in seconds)
    scroll_delay: float = 1.0

    # Request throttling settings (in seconds)
    page_delay: float = 2.0  # Delay between capturing pages
    request_delay: float = 0.5  # Delay between requests during page load
    enable_request_throttling: bool = False  # Enable/disable request throttling (disabled by default due to Playwright event loop blocking)

    # Viewport settings
    viewport_width: Optional[int] = None
    viewport_height: Optional[int] = None
    viewport_auto_adjust: bool = False
    max_viewport_width: int = 7680
    max_viewport_height: int = 43200

    # Browser settings
    headless: bool = True

    # Logging settings
    verbose: bool = False

    @classmethod
    def from_yaml(cls, config_file: str) -> "ScreenShotConfig":
        """
        Load configuration from YAML file.

        Args:
            config_file: Path to YAML configuration file

        Returns:
            ScreenShotConfig instance

        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If config file format is invalid
        """
        try:
            with open(config_file, 'r') as f:
                config_dict = yaml.safe_load(f) or {}

            # Flatten nested config structure
            flattened_config = cls._flatten_config(config_dict)

            # Filter only valid config parameters
            valid_params = {k: v for k, v in flattened_config.items()
                          if k in cls.__dataclass_fields__}

            return cls(**valid_params)
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file not found: {config_file}")
        except Exception as e:
            raise ValueError(f"Failed to load config from {config_file}: {e}")

    @staticmethod
    def _flatten_config(config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Flatten nested YAML config structure to flat parameter dict.

        Args:
            config: Nested configuration dictionary

        Returns:
            Flattened configuration dictionary
        """
        flattened = {}

        # Browser settings
        if 'browser' in config:
            flattened['headless'] = config['browser'].get('headless', 60000)

        # Timeout settings
        if 'timeouts' in config:
            flattened['navigation_timeout'] = config['timeouts'].get('navigation_timeout', 60000)
            flattened['action_timeout'] = config['timeouts'].get('action_timeout', 60000)
            flattened['final_wait'] = config['timeouts'].get('final_wait', 5000)

        # Scroll settings
        if 'scroll' in config:
            flattened['scroll_delay'] = config['scroll'].get('delay', 1.0)

        # Request throttling settings
        if 'throttling' in config:
            flattened['page_delay'] = config['throttling'].get('page_delay', 2.0)
            flattened['request_delay'] = config['throttling'].get('request_delay', 0.5)
            flattened['enable_request_throttling'] = config['throttling'].get('enable_request_throttling', True)

        # Viewport settings
        if 'viewport' in config:
            flattened['viewport_width'] = config['viewport'].get('width')
            flattened['viewport_height'] = config['viewport'].get('height')
            flattened['viewport_auto_adjust'] = config['viewport'].get('auto_adjust', False)
            flattened['max_viewport_width'] = config['viewport'].get('max_width', 7680)
            flattened['max_viewport_height'] = config['viewport'].get('max_height', 43200)

        # Logging settings
        if 'logging' in config:
            flattened['verbose'] = config['logging'].get('verbose', False)

        return flattened

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary representation."""
        return asdict(self)


class WebScreenShot:
    """
    A reusable class for capturing full-page screenshots of websites using Playwright.

    Features:
    - URL validation with blank image fallback for invalid URLs
    - Configurable timeouts and delays
    - Custom viewport support with auto-adjustment
    - Reusable browser instance for multiple screenshots
    - Logging support for debugging
    - Handles lazy-loaded images
    - Configuration file support (YAML)
    - Viewport auto-adjustment to capture entire page in one screenshot
    """

    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize the WebScreenShot instance.

        Args:
            config_file: Path to YAML configuration file. If None, uses default configuration.

        Raises:
            ValueError: If config file format is invalid

        Examples:
            # Using config file
            screenshot = WebScreenShot(config_file='web_screenshot_config.yaml')

            # Using default configuration
            screenshot = WebScreenShot()
        """
        if config_file:
            try:
                self.config = ScreenShotConfig.from_yaml(config_file)
            except Exception as e:
                raise ValueError(f"Failed to initialize WebScreenShot: {e}")
        else:
            # Use default configuration
            self.config = ScreenShotConfig()

        # Setup logging
        self.logger = logging.getLogger(__name__)
        if self.config.verbose:
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        else:
            logging.basicConfig(level=logging.WARNING)

        # Browser instance management
        self._playwright = None
        self._browser: Optional[Browser] = None
        self._is_open = False

    # Convenience properties for backward compatibility
    @property
    def navigation_timeout(self) -> int:
        return self.config.navigation_timeout

    @property
    def action_timeout(self) -> int:
        return self.config.action_timeout

    @property
    def scroll_delay(self) -> float:
        return self.config.scroll_delay

    @property
    def page_delay(self) -> float:
        return self.config.page_delay

    @property
    def request_delay(self) -> float:
        return self.config.request_delay

    @property
    def enable_request_throttling(self) -> bool:
        return self.config.enable_request_throttling

    @property
    def final_wait(self) -> int:
        return self.config.final_wait

    @property
    def viewport_width(self) -> Optional[int]:
        return self.config.viewport_width

    @property
    def viewport_height(self) -> Optional[int]:
        return self.config.viewport_height

    @property
    def viewport_auto_adjust(self) -> bool:
        return self.config.viewport_auto_adjust

    @property
    def max_viewport_width(self) -> int:
        return self.config.max_viewport_width

    @property
    def max_viewport_height(self) -> int:
        return self.config.max_viewport_height

    @property
    def headless(self) -> bool:
        return self.config.headless

    @property
    def verbose(self) -> bool:
        return self.config.verbose

    def __enter__(self):
        """Context manager entry."""
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    def open(self):
        """Open the browser instance."""
        if not self._is_open:
            self.logger.info("Launching browser...")
            self._playwright = sync_playwright().start()
            self._browser = self._playwright.chromium.launch(headless=self.headless)
            self._is_open = True
            self.logger.info("Browser launched successfully")

    def close(self):
        """Close the browser instance."""
        if self._is_open:
            self.logger.info("Closing browser...")
            if self._browser:
                self._browser.close()
            if self._playwright:
                self._playwright.stop()
            self._is_open = False
            self.logger.info("Browser closed")

    def capture_multiple_pages(self, url: str, output_dir: Optional[str] = None) -> bool:
        """
        Capture multiple pages of a webpage as separate PNG files.
        Each page is captured in viewport-sized chunks (no auto-adjust).

        Args:
            url: URL of the webpage to capture
            output_dir: Directory where screenshots will be saved.
                       If None, defaults to current directory.

        Returns:
            True if capture was successful, False if URL was invalid (blank image created)
        """
        # Generate default directory with timestamp if not provided
        if output_dir is None:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            output_dir = f"screenshots_{timestamp}"

        # Create output directory
        try:
            Path(output_dir).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            self.logger.error(f"Error creating output directory: {e}")
            return False

        # Validate URL
        if not self._is_valid_url(url):
            self.logger.warning(f"Invalid URL provided: {url}. Creating blank image.")
            self._create_blank_image(str(Path(output_dir) / "page_1.png"))
            return False

        page = None
        try:
            self.logger.info(f"Starting multi-page capture for: {url}")
            page = self._setup_page(auto_adjust=False)

            # Navigate to URL
            self.logger.info(f"Navigating to {url}...")
            page.goto(url)

            # Wait for initial load
            page.wait_for_load_state('networkidle')

            # Scroll and load lazy content
            self._scroll_and_load(page)

            # Get page dimensions
            total_height = page.evaluate('document.body.scrollHeight')
            viewport_height = page.evaluate('window.innerHeight')

            self.logger.info(f"Page height: {total_height}px, Viewport height: {viewport_height}px")

            # Calculate number of pages needed
            num_pages = (total_height + viewport_height - 1) // viewport_height
            self.logger.info(f"Capturing {num_pages} page(s)...")

            # Capture each page
            for page_num in range(num_pages):
                # Add delay between page captures to avoid rate limiting
                if page_num > 0:
                    self.logger.info(f"Waiting {self.page_delay}s before capturing next page...")
                    time.sleep(self.page_delay)

                # Scroll to position
                scroll_position = page_num * viewport_height
                page.evaluate(f'window.scrollTo(0, {scroll_position})')

                # Wait for load and dismiss popups
                page.wait_for_load_state('networkidle')
                self._dismiss_popups(page)
                page.wait_for_timeout(self.final_wait)

                # Capture screenshot
                output_path = str(Path(output_dir) / f"page_{page_num + 1}.png")
                self.logger.info(f"Capturing page {page_num + 1}/{num_pages} to {output_path}...")
                page.screenshot(path=output_path)

            self.logger.info(f"Multi-page capture completed. {num_pages} pages saved to {output_dir}")
            return True

        except Exception as e:
            self.logger.error(f"Error capturing multiple pages: {e}")
            return False

        finally:
            if page:
                page.close()

    def capture(self, url: str, output_path: Optional[str] = None, auto_adjust: Optional[bool] = None) -> bool:
        """
        Capture a full-page screenshot of the given URL.

        Args:
            url: URL of the webpage to capture
            output_path: Path where the screenshot will be saved.
                        If None, defaults to "screenshot_YYYYMMDD_HHMMSS.png"
            auto_adjust: Override the viewport_auto_adjust setting for this capture.
                        If None, uses the instance setting.

        Returns:
            True if screenshot was successful, False if URL was invalid (blank image created)
        """
        # Generate default filename with timestamp if not provided
        if output_path is None:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            output_path = f"screenshot_{timestamp}.png"

        # Validate URL
        if not self._is_valid_url(url):
            self.logger.warning(f"Invalid URL provided: {url}. Creating blank image.")
            self._create_blank_image(output_path)
            return False

        # Determine if we should auto-adjust viewport
        use_auto_adjust = auto_adjust if auto_adjust is not None else self.viewport_auto_adjust

        page = None
        try:
            self.logger.info(f"Starting screenshot capture for: {url}")
            page = self._setup_page(auto_adjust=use_auto_adjust)

            # Navigate to URL
            self.logger.info(f"Navigating to {url}...")
            page.goto(url)

            # Wait for initial load
            page.wait_for_load_state('networkidle')

            if use_auto_adjust:
                # Adjust viewport to page dimensions for single-screenshot capture
                self._adjust_viewport_to_page(page)
                self.logger.info("Viewport adjusted - entire page will be captured in one screenshot")
            else:
                # Scroll and load lazy content (traditional method)
                self._scroll_and_load(page)

            # Wait for network idle and add extra buffer time
            self.logger.info("Waiting for network idle...")
            page.wait_for_load_state('networkidle')
            page.wait_for_timeout(self.final_wait)

            # Take screenshot
            self.logger.info(f"Capturing screenshot to {output_path}...")
            if use_auto_adjust:
                # With auto-adjust, we don't need full_page=True since viewport matches page
                page.screenshot(path=output_path)
            else:
                # Traditional full-page screenshot
                page.screenshot(path=output_path, full_page=True)
            self.logger.info("Screenshot captured successfully")

            return True

        except Exception as e:
            self.logger.error(f"Error capturing screenshot: {e}")
            self.logger.warning("Creating blank image due to error")
            self._create_blank_image(output_path)
            return False

        finally:
            if page:
                page.close()

    # Private helper methods

    def _is_valid_url(self, url: str) -> bool:
        """
        Validate if the URL is properly formed.

        Args:
            url: URL string to validate

        Returns:
            True if valid, False otherwise
        """
        try:
            result = urlparse(url)
            is_valid = all([result.scheme, result.netloc]) and result.scheme in ['http', 'https']
            if not is_valid:
                self.logger.warning(f"Invalid URL: {url}")
            return is_valid
        except Exception as e:
            self.logger.error(f"URL validation error: {e}")
            return False

    def _create_blank_image(self, output_path: str, width: int = 800, height: int = 600):
        """
        Create a blank white image.

        Args:
            output_path: Path to save the blank image
            width: Image width in pixels (default: 800)
            height: Image height in pixels (default: 600)
        """
        self.logger.info(f"Creating blank image at {output_path}")
        blank_image = Image.new('RGB', (width, height), color='white')
        blank_image.save(output_path)

    def _setup_page(self, auto_adjust: bool = False) -> Page:
        """
        Create and configure a new page instance.

        Args:
            auto_adjust: If True, skip initial viewport config for auto-adjustment

        Returns:
            Configured Page object
        """
        if not self._is_open:
            self.open()

        viewport_config = {}
        # Only set viewport if not using auto-adjust, or if specific dimensions are provided
        if not auto_adjust:
            if self.viewport_width is not None:
                viewport_config['width'] = self.viewport_width
            if self.viewport_height is not None:
                viewport_config['height'] = self.viewport_height

        page = self._browser.new_page(viewport=viewport_config if viewport_config else None)
        page.set_default_navigation_timeout(self.navigation_timeout)
        page.set_default_timeout(self.action_timeout)

        # Add request throttling to avoid rate limiting (if enabled)
        if self.enable_request_throttling:
            page.route("**/*", self._throttle_request)

        return page

    def _throttle_request(self, route):
        """
        Throttle requests with delay to avoid rate limiting.

        Args:
            route: Playwright route object
        """
        time.sleep(self.request_delay)
        route.continue_()

    def _dismiss_popups(self, page: Page):
        """
        Attempt to dismiss common popup types (alerts, modals, cookie notices, etc).

        Args:
            page: Playwright Page object
        """
        try:
            # Dismiss alert dialogs if present
            page.on("dialog", lambda dialog: dialog.dismiss())

            # Try to find and close common popup selectors
            popup_selectors = [
                # Close buttons
                "button[aria-label='Close']",
                "button.close",
                "button[type='button'][aria-label*='close' i]",
                "[role='button'][aria-label*='close' i]",
                # Common modal close buttons
                ".modal-close",
                ".popup-close",
                "[class*='close-btn']",
                "[class*='dismiss']",
                # Cookie notices
                ".cookie-notice button[type='button']",
                "[data-testid='cookie-accept']",
                # Rate limit popups (generic)
                "[role='alertdialog'] button",
                "[role='dialog'] button:first-of-type",
            ]

            for selector in popup_selectors:
                try:
                    elements = page.query_selector_all(selector)
                    for element in elements:
                        if element and element.is_visible():
                            self.logger.debug(f"Closing popup with selector: {selector}")
                            element.click()
                            time.sleep(0.3)
                except Exception:
                    pass

        except Exception as e:
            self.logger.debug(f"Error dismissing popups: {e}")

    def _adjust_viewport_to_page(self, page: Page):
        """
        Adjust viewport dimensions to match the full page dimensions.
        This allows capturing the entire page in one screenshot without scrolling.

        Args:
            page: Playwright Page object
        """
        self.logger.info("Auto-adjusting viewport to page dimensions...")

        # Get the actual page dimensions
        page_width = page.evaluate('document.documentElement.scrollWidth')
        page_height = page.evaluate('document.documentElement.scrollHeight')

        # Apply max limits for safety
        adjusted_width = min(page_width, self.max_viewport_width)
        adjusted_height = min(page_height, self.max_viewport_height)

        self.logger.info(f"Page dimensions: {page_width}x{page_height}")
        self.logger.info(f"Adjusted viewport: {adjusted_width}x{adjusted_height}")

        # Set the new viewport size
        page.set_viewport_size({
            'width': adjusted_width,
            'height': adjusted_height
        })

        # Reload the page with new viewport
        page.reload()
        page.wait_for_load_state('networkidle')

    def _scroll_and_load(self, page: Page):
        """
        Scroll through the page to trigger lazy-loaded content.

        Args:
            page: Playwright Page object
        """
        self.logger.info("Starting page scroll to trigger lazy-loaded content...")

        # Force all lazy-loaded images to load eagerly
        page.evaluate('''() => {
            document.querySelectorAll('img[loading="lazy"]').forEach(img => img.setAttribute('loading', 'eager'));
        }''')

        # Incrementally scroll down the page
        viewport_height = page.evaluate('window.innerHeight')
        total_height = page.evaluate('document.body.scrollHeight')
        scroll_position = 0

        while scroll_position < total_height:
            scroll_position += viewport_height
            page.evaluate(f'window.scrollTo(0, {scroll_position})')
            self.logger.debug(f"Scrolled to position: {scroll_position}/{total_height}")
            time.sleep(self.scroll_delay)
            total_height = page.evaluate('document.body.scrollHeight')

        self.logger.info("Page scroll completed")


# Module-level convenience functions

def screenshot(url: str, config_file: str, output_path: Optional[str] = None) -> bool:
    """
    Simple convenience function for quick screenshots.

    Args:
        url: URL to capture
        config_file: Path to YAML configuration file
        output_path: Where to save (default: auto-generated timestamp)

    Returns:
        True if successful, False otherwise

    Example:
        screenshot("https://example.com", "web_screenshot_config.yaml", "output.png")
    """
    with WebScreenShot(config_file) as shot:
        return shot.capture(url, output_path)




# Command-line interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='Capture full-page screenshots of websites using Playwright',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic single screenshot (viewport-based)
  python web_screenshot.py --url https://example.com

  # With custom output path
  python web_screenshot.py --url https://example.com --output output.png

  # Capture entire webpage in one screenshot (auto-adjust viewport)
  python web_screenshot.py --url https://example.com --full-page

  # Capture all pages as separate PNG files
  python web_screenshot.py --url https://example.com --multi-page

  # Capture all pages with custom output directory
  python web_screenshot.py --url https://example.com --multi-page --output screenshots_dir
        """
    )

    parser.add_argument('--url', '-u', required=True, help='URL of the webpage to capture')
    parser.add_argument('--output', '-o', help='Output path/directory for screenshot(s)')
    parser.add_argument('--full-page', '-f', action='store_true',
                        help='Capture entire webpage in one screenshot by auto-adjusting viewport')
    parser.add_argument('--multi-page', '-m', action='store_true',
                        help='Capture all pages as separate PNG files in a directory')

    args = parser.parse_args()

    # Validate conflicting flags
    if args.full_page and args.multi_page:
        print("Error: Cannot use --full-page and --multi-page together")
        sys.exit(1)

    try:
        shot = WebScreenShot()

        if args.multi_page:
            # Capture multiple pages
            success = shot.capture_multiple_pages(args.url, args.output)
            if success:
                final_path = args.output if args.output else 'screenshots_<timestamp>'
                print(f"Screenshots saved to {final_path}")
            else:
                print(f"Failed to capture multiple pages")
        elif args.full_page:
            # Capture entire webpage in one screenshot
            shot.config = ScreenShotConfig(viewport_auto_adjust=True)
            success = shot.capture(args.url, args.output)
            if success:
                final_path = args.output if args.output else 'screenshot_<timestamp>.png'
                print(f"Screenshot saved to {final_path}")
            else:
                print(f"Invalid URL. Blank image saved to {final_path}")
        else:
            # Default: single viewport screenshot
            success = shot.capture(args.url, args.output)
            if success:
                final_path = args.output if args.output else 'screenshot_<timestamp>.png'
                print(f"Screenshot saved to {final_path}")
            else:
                final_path = args.output if args.output else 'screenshot_<timestamp>.png'
                print(f"Invalid URL. Blank image saved to {final_path}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
