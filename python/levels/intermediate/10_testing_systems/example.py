import unittest
from unittest.mock import Mock

def notify(sender, message): sender(message)
class Tests(unittest.TestCase):
    def test_notify(self):
        sender = Mock(); notify(sender, "done"); sender.assert_called_once_with("done")
if __name__ == "__main__": unittest.main()
