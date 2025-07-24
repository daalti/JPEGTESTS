import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using knhgf.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:knhgf.obj=b1c35b2afb989f62c202ec3c2887b4a87182deb610f5147b76ab5b33d57ccf33
    +test_classification:System
    +name: test_pcl5_hpgl_char_tt_2bytetypeface_knhgf
    +test:
        +title: test_pcl5_hpgl_char_tt_2bytetypeface_knhgf
        +guid:d2b64e0a-468d-4976-85c8-d753218da1dc
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_tt_2bytetypeface_knhgf(setup_teardown, printjob, outputsaver):
    printjob.print_verify('b1c35b2afb989f62c202ec3c2887b4a87182deb610f5147b76ab5b33d57ccf33', timeout=600)
    outputsaver.save_output()
