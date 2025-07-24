import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using pa_igm.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:pa_igm.obj=82885883bfe9b077072daa414f88fd00d0f73f9a5ae002501e3c211d7a2837e0
    +test_classification:System
    +name: test_pcl5_hpgl_vector_pa_igm
    +test:
        +title: test_pcl5_hpgl_vector_pa_igm
        +guid:1a5563b2-9e0c-4138-b925-eaa76de054a3
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_vector_pa_igm(setup_teardown, printjob, outputsaver):
    printjob.print_verify('82885883bfe9b077072daa414f88fd00d0f73f9a5ae002501e3c211d7a2837e0', timeout=600)
    outputsaver.save_output()
