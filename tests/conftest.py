import pytest


@pytest.fixture
def test_html():
    return '''
<html>
  <head>
    <script type="text/javascript" src="test-site"></script>
    <link rel="alternate" type="text/rss" src="test-rss">
  </head>
  <body>
    <div class="testlinks">
      <a href="https://mac.test.com/" title="Mac Software"><i class="fa fa-apple faded"></i> Mac</a>
      <a href="https://mac.test.com/test.zip" title="Mac Software"><i class="fa fa-apple faded"></i> Mac</a>
      <a href="https://mac.test.com/download/test.dmg" title="Mac Software"><i class="fa fa-apple faded"></i> Mac</a>
      <a href="https://mac.test.com/download/test-1.0.0.tar.gz" title="Mac Software"><i class="fa fa-apple faded"></i> Mac</a>
      <a href="https://mac.test.com/download/test-1.0.0.tar.gz" title="Mac Software"><i class="fa fa-apple faded"></i> Mac</a>
    </div>
  </body>
</html>
'''