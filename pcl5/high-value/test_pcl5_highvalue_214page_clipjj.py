import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 214Page_clipjj.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:3600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:214Page-clipjj.obj=d6fccada3771a6dcea6573c3b8e874a66e75939fd7e05fb911b37797a3c22c06
    +test_classification:System
    +name: test_pcl5_highvalue_214page_clipjj
    +test:
        +title: test_pcl5_highvalue_214page_clipjj
        +guid:3d5fe225-de3e-454e-82ff-c495fda03820
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_214page_clipjj(setup_teardown, printjob, outputsaver,tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_legal_8.5x14in', default):
        tray.configure_tray(default, 'na_legal_8.5x14in','stationery')
    printjob.print_verify('d6fccada3771a6dcea6573c3b8e874a66e75939fd7e05fb911b37797a3c22c06', timeout=36000)
    outputsaver.save_output()
