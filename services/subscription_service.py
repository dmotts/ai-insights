import logging

class SubscriptionService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.subscribers = []

    def add_subscriber(self, email: str, industry: str):
        if email not in [subscriber['email'] for subscriber in self.subscribers]:
            self.subscribers.append({'email': email, 'industry': industry})
            self.logger.info(f"Subscriber added: {email} for industry {industry}")
        else:
            self.logger.warning(f"Subscriber already exists: {email}")

    def remove_subscriber(self, email: str):
        self.subscribers = [subscriber for subscriber in self.subscribers if subscriber['email'] != email]
        self.logger.info(f"Subscriber removed: {email}")

    def send_trend_updates(self):
        for subscriber in self.subscribers:
            email = subscriber['email']
            industry = subscriber['industry']
            trend_analysis = self.perform_trend_analysis(industry)
            # Logic to send trend updates to subscribers
            self.logger.info(f"Sending trend update to {email} for industry {industry}")

    def perform_trend_analysis(self, industry: str) -> str:
        """
        Analyze trends for the given industry to provide updates.
        """
        # Placeholder for trend analysis logic
        return f"Latest trends and updates in {industry}"
