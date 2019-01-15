import unittest

from unittests.api_admin_tests import ApiAdminTests
from unittests.api_fs_tests import ApiFsTests

from unittests.api_wms_tests import ApiWmsTests

from unittests.db_tests import DbTests

from unittests.ui_account_tests import UiAccountTests
from unittests.ui_application_tests import UiApplicationTests
from unittests.ui_auth_tests import UiAuthTests
from unittests.ui_docs_tests import UiDocsTests
from unittests.ui_errors_tests import UiErrorsTests
from unittests.ui_explorer_tests import UiExplorerTests
from unittests.ui_feed_tests import UiFeedTests
from unittests.ui_profile_tests import UiProfileTests

from unittests.plugin_general_tests import PluginGeneralTests
from unittests.plugin_loader_tests import PluginLoaderTests
from unittests.plugin_proxy_tests import PluginProxyTests
from unittests.plugin_translation_tests import PluginTranslationTests

unittest.main(verbosity=2)
