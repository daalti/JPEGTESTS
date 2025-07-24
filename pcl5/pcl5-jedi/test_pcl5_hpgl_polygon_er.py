import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using er.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:er.obj=bb97d8dce896020cf63874d74f408b7ea8dd3f56ceb8d88bda75775152761895
    +test_classification:System
    +name: test_pcl5_hpgl_polygon_er
    +test:
        +title: test_pcl5_hpgl_polygon_er
        +guid:c4c7d73e-ec07-4689-a0ca-6c01d0c1baf6
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_polygon_er(setup_teardown, printjob, outputsaver):
    printjob.print_verify('bb97d8dce896020cf63874d74f408b7ea8dd3f56ceb8d88bda75775152761895', timeout=600)
    outputsaver.save_output()
