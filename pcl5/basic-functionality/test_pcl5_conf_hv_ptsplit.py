import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:PCL5 high value test using **ptsplit.cht
    +test_tier: 3
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-156300
    +timeout:180
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework:TUF
    +external_files:ptsplit.cht=b0cdada29f7a7e50ac815c03e606b2a3c3e53c944ac29053ce0c656dad153303
    +name:test_pcl5_conf_hv_ptsplit
    +test:
        +title:test_pcl5_conf_hv_ptsplit
        +guid:f0887048-a9c1-44ad-911e-acedc1106c20
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_conf_hv_ptsplit(setup_teardown, printjob, outputverifier):
    printjob.print_verify('b0cdada29f7a7e50ac815c03e606b2a3c3e53c944ac29053ce0c656dad153303')
    outputverifier.save_and_parse_output()
