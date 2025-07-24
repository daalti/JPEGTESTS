import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 20Page_fontpri4.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:20Page-fontpri4.obj=cb8ebf0cf1ceb50a6413b71002257799c51ccd4301b6a06de54331812e906ce6
    +test_classification:System
    +name: test_pcl5_lowvaluenew_20page_fontpri4
    +test:
        +title: test_pcl5_lowvaluenew_20page_fontpri4
        +guid:a83e7ae5-2451-4862-aa1e-199313c7e886
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_lowvaluenew_20page_fontpri4(setup_teardown, printjob, outputsaver):
    printjob.print_verify('cb8ebf0cf1ceb50a6413b71002257799c51ccd4301b6a06de54331812e906ce6', timeout=600)
    outputsaver.save_output()
