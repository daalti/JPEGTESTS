import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 5Page_space.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:5Page-space.obj=0409c38a78fd0e8de1d75f22db47ab545bfcd3e791426049a68f0764ca4e00a2
    +test_classification:System
    +name: test_pcl5_lowvaluenew_5page_space
    +test:
        +title: test_pcl5_lowvaluenew_5page_space
        +guid:bf2d1495-f0ac-4edd-8cc5-daadea43bfc8
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_lowvaluenew_5page_space(setup_teardown, printjob, outputsaver):
    printjob.print_verify('0409c38a78fd0e8de1d75f22db47ab545bfcd3e791426049a68f0764ca4e00a2', timeout=600)
    outputsaver.save_output()
