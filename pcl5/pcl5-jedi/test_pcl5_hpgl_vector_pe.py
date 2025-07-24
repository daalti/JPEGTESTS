import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using pe.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:pe.obj=1fba5081319e64ad34ae42dfe02819820a73be3068397c7eedc3323d66daf7f7
    +test_classification:System
    +name: test_pcl5_hpgl_vector_pe
    +test:
        +title: test_pcl5_hpgl_vector_pe
        +guid:39aec58d-fdb7-4c60-aacb-5e98381781b5
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_vector_pe(setup_teardown, printjob, outputsaver):
    printjob.print_verify('1fba5081319e64ad34ae42dfe02819820a73be3068397c7eedc3323d66daf7f7', timeout=600)
    outputsaver.save_output()
