import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using knhbf.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:knhbf.obj=2c177936a83a5192d07f910154949d1829c41df53222f77cf1c60f650646ba57
    +test_classification:System
    +name: test_pcl5_hpgl_char_tt_2bytetypeface_knhbf
    +test:
        +title: test_pcl5_hpgl_char_tt_2bytetypeface_knhbf
        +guid:64940ee9-16be-43af-8a06-c06abd828925
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_tt_2bytetypeface_knhbf(setup_teardown, printjob, outputsaver):
    printjob.print_verify('2c177936a83a5192d07f910154949d1829c41df53222f77cf1c60f650646ba57', timeout=600)
    outputsaver.save_output()
