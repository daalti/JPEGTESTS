import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using ft2.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ft2.obj=b0d4147e3dde1d24d5020aece1d3e0e71d43bc8e6b1174fb98c727fc5e0da6d8
    +test_classification:System
    +name: test_pcl5_hpgl_lfatt_ft2
    +test:
        +title: test_pcl5_hpgl_lfatt_ft2
        +guid:c736602b-9a47-4466-81a0-3516df172933
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_lfatt_ft2(setup_teardown, printjob, outputsaver):
    printjob.print_verify('b0d4147e3dde1d24d5020aece1d3e0e71d43bc8e6b1174fb98c727fc5e0da6d8', timeout=600)
    outputsaver.save_output()
