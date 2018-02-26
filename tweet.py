import twitter
import logging


class Tweeter:
    def __init__(self, t: twitter.Twitter) -> None:
        self.connection = t
        self.logger = logging.getLogger('tweet')

    def tweet(self, new_post: str) -> None:
        status = f"Check out our latest blog post: {new_post}"

        try:
            self.connection.statuses.update(status=status)
            self.logger.info('Successfully created new tweet.')
        except twitter.TwitterError:
            self.logger.error('An error occurred while creating tweet.')
