from datetime import datetime
import geoip2.database
import logging

class UtilitiesService:
    """Service class for utility functions."""

    def __init__(self, geoip_db_path: str):
        self.geoip_db_path = geoip_db_path
        self.logger = logging.getLogger(__name__)

    def get_current_year(self) -> int:
        """Returns the current year."""
        return datetime.now().year

    def generate_report_id(self) -> str:
        """Generates a unique report ID based on the current timestamp."""
        return str(int(datetime.now().timestamp()))

    def get_current_timestamp(self) -> str:
        """Returns the current timestamp in ISO format."""
        return datetime.now().isoformat()

    def get_location(self, ip_address: str) -> str:
        """Returns the city and country of the given IP address using the GeoLite2 database."""
        try:
            with geoip2.database.Reader(self.geoip_db_path) as reader:
                response = reader.city(ip_address)
                country = response.country.name
                city = response.city.name
                return f"{city}, {country}" if city else country
        except Exception as e:
            self.logger.error(f"Error getting location for IP {ip_address}: {e}")
            return "Unknown"

    def extract_user_info(self, request) -> dict:
        """Extracts user information from the request headers."""
        ip_address = request.remote_addr
        location = self.get_location(ip_address)
        user_info = {
            "ip_address": ip_address,
            "location": location,
            "device": request.headers.get('User-Agent'),
            "language": request.headers.get('Accept-Language'),
            "referrer": request.headers.get('Referer'),
            "request_time": self.get_current_timestamp()
        }
        return user_info
