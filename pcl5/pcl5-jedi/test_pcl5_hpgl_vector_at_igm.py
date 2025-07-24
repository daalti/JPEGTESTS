import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using at_igm.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:at_igm.obj=d1a74fef6e01bc0be2eeed8059f356bae3be3d5faac942898b4d4458eb93cb2a
    +test_classification:System
    +name: test_pcl5_hpgl_vector_at_igm
    +test:
        +title: test_pcl5_hpgl_vector_at_igm
        +guid:2576522a-0de8-4686-83cc-acd723dd2513
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_vector_at_igm(setup_teardown, printjob, outputsaver):
    printjob.print_verify('d1a74fef6e01bc0be2eeed8059f356bae3be3d5faac942898b4d4458eb93cb2a', timeout=600)
    outputsaver.save_output()
