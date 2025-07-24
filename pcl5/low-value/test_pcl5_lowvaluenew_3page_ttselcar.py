import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 3Page_ttselcar.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:3Page-ttselcar.obj=7565da355f44a331582e085326793878aca9653294faf6573bda11ce7df0daf9
    +test_classification:System
    +name: test_pcl5_lowvaluenew_3page_ttselcar
    +test:
        +title: test_pcl5_lowvaluenew_3page_ttselcar
        +guid:0aeb4b96-9797-41a4-96fe-7e907ed6b8cf
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_lowvaluenew_3page_ttselcar(setup_teardown, printjob, outputsaver):
    printjob.print_verify('7565da355f44a331582e085326793878aca9653294faf6573bda11ce7df0daf9', timeout=600)
    outputsaver.save_output()
