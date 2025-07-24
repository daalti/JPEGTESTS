import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using tchpmlv.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:tchpmlv.obj=c802eb762eb81f0a83baf16168e90f53257d6444c63c4a17b7ee76dd69767e05
    +test_classification:System
    +name: test_pcl5_hpgl_char_tt_2bytetypeface_tchpmlv
    +test:
        +title: test_pcl5_hpgl_char_tt_2bytetypeface_tchpmlv
        +guid:557d2413-24af-4773-bf96-1e693e4cab66
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_tt_2bytetypeface_tchpmlv(setup_teardown, printjob, outputsaver):
    printjob.print_verify('c802eb762eb81f0a83baf16168e90f53257d6444c63c4a17b7ee76dd69767e05', timeout=600)
    outputsaver.save_output()
