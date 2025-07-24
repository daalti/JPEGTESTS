import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 87Page_ttfdes.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:87Page-ttfdes.obj=39abc1768240389d00186c199fdddaefec5d091230838967753a8266eec58776
    +test_classification:System
    +name: test_pcl5_lowvaluenew_87page_ttfdes
    +test:
        +title: test_pcl5_lowvaluenew_87page_ttfdes
        +guid:495a6e59-d7e7-4a4c-9a6a-3bca69219100
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_lowvaluenew_87page_ttfdes(setup_teardown, printjob, outputsaver):
    printjob.print_verify('39abc1768240389d00186c199fdddaefec5d091230838967753a8266eec58776', timeout=600)
    outputsaver.save_output()
