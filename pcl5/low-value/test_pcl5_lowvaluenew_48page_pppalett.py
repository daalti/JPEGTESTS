import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 48Page_pppalett.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:48Page-pppalett.obj=0c5363651d460066cd824432969e27257efa3500d9bccb1bd8cc400dcae153b9
    +test_classification:System
    +name: test_pcl5_lowvaluenew_48page_pppalett
    +test:
        +title: test_pcl5_lowvaluenew_48page_pppalett
        +guid:1034f805-f962-4a7a-ace2-148f17836412
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_lowvaluenew_48page_pppalett(setup_teardown, printjob, outputsaver):
    printjob.print_verify('0c5363651d460066cd824432969e27257efa3500d9bccb1bd8cc400dcae153b9', timeout=600)
    outputsaver.save_output()
