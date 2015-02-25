import unittest
import textwrap

from tcslackbot import bot


class TestCase(unittest.TestCase):

    def test_look_for_urls_multiple(self):
        """
        multiple matches, yeild them all
        """
        msg = textwrap.dedent("""
            some stuff http://localhost:8111/viewLog.html?buildId=4&
            buildTypeId=TcSlackBotTests_Test&tab=buildResultsDiv more stuff\n
            another line http://localhost:8111/viewLog.html?buildId=99&
            buildTypeId=TcSlackBotTests_Test&tab=buildResultsDiv more stuff\n
            """)

        urls = [url for url in bot.look_for_urls(msg)]
        self.assertEqual(
            urls,
            ['http://localhost:8111/httpAuth/app/rest/builds/id:4',
             'http://localhost:8111/httpAuth/app/rest/builds/id:99'])


if __name__ == '__main__':
    unittest.main()
