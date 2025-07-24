import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using knhdf.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:knhdf.obj=807994a367cb74392914464659a77862bea7afecf9efa9690579cbb6801a1b67
    +test_classification:System
    +name: test_pcl5_hpgl_char_tt_2bytetypeface_knhdf
    +test:
        +title: test_pcl5_hpgl_char_tt_2bytetypeface_knhdf
        +guid:c6ba10c0-f190-421d-af18-7ed91ffea57f
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_tt_2bytetypeface_knhdf(setup_teardown, printjob, outputsaver):
    printjob.print_verify('807994a367cb74392914464659a77862bea7afecf9efa9690579cbb6801a1b67', timeout=600)
    outputsaver.save_output()
