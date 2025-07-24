import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using fn.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:fn.obj=7275ce3dfae332bdf0e03b5f272117abde8a1c49d9e5121aec4fcad4766e8acb
    +test_classification:System
    +name: test_pcl5_hpgl_char_fn
    +test:
        +title: test_pcl5_hpgl_char_fn
        +guid:4ed6e3b2-89fe-4641-aece-5e8fe4858248
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_fn(setup_teardown, printjob, outputsaver):
    printjob.print_verify('7275ce3dfae332bdf0e03b5f272117abde8a1c49d9e5121aec4fcad4766e8acb', timeout=600)
    outputsaver.save_output()
