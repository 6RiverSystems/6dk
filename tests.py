import unittest

from unittests.api_admin_tests import ApiAdminTests
from unittests.api_fs_tests import ApiFsTests
from unittests.api_wms_tests import ApiWmsTests

from unittests.db_tests import DbTests

from unittests.ui_tests import UiTests

from unittests.plugin_general_tests import PluginGeneralTests
from unittests.plugin_loader_tests import PluginLoaderTests
from unittests.plugin_proxy_tests import PluginProxyTests
from unittests.plugin_translation_tests import PluginTranslationTests

unittest.main(verbosity=2)
