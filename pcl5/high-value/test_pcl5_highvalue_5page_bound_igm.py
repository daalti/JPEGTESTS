import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 5Page_bound_igm.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:320
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:5Page-bound_igm.obj=2aaee9da5065934f4fb16979bee5f302de77cbd99ba66db51a53b3b58454076a
    +test_classification:System
    +name: test_pcl5_highvalue_5page_bound_igm
    +test:
        +title: test_pcl5_highvalue_5page_bound_igm
        +guid:f8fa2fc3-76a9-4884-8eee-159b4f22289a
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_5page_bound_igm(udw, setup_teardown, printjob, outputsaver):
    # printjob.print_verify('2aaee9da5065934f4fb16979bee5f302de77cbd99ba66db51a53b3b58454076a',timeout=320, expected_jobs=4)
    # outputsaver.save_output()
    outputsaver.operation_mode('TIFF')
    udw_result = udw.mainApp.execute('PrintAppUw PUB_isUelAsNewJob')
    if(int(udw_result)):
        printjob.print_verify_multi('2aaee9da5065934f4fb16979bee5f302de77cbd99ba66db51a53b3b58454076a', timeout=320,expected_jobs=4)
    else:
        printjob.print_verify('2aaee9da5065934f4fb16979bee5f302de77cbd99ba66db51a53b3b58454076a', timeout=320)
    outputsaver.save_output()
