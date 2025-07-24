import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using sa.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:sa.obj=2ad5744b2f71d3c190bf9967a51e82b7a1aa99a56472d478f8f413ae667aca9e
    +test_classification:System
    +name: test_pcl5_hpgl_char_sa
    +test:
        +title: test_pcl5_hpgl_char_sa
        +guid:28523854-a28c-4d1e-971d-1e15ec30e204
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_sa(setup_teardown, printjob, outputsaver):
    printjob.print_verify('2ad5744b2f71d3c190bf9967a51e82b7a1aa99a56472d478f8f413ae667aca9e', timeout=600)
    outputsaver.save_output()
