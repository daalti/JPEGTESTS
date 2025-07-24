import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 1Page_tgen_ac_7.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:1Page-tgen_ac_7.obj=fabe938f145c48254481f90658198046abd21ebdce94e833eea805b665100de5
    +test_classification:System
    +name: test_pcl5_highvalue_1page_tgen_ac_7
    +test:
        +title: test_pcl5_highvalue_1page_tgen_ac_7
        +guid:54772b65-1236-4216-ab44-709a4b1f0541
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_1page_tgen_ac_7(setup_teardown, printjob, outputsaver):
    printjob.print_verify('fabe938f145c48254481f90658198046abd21ebdce94e833eea805b665100de5', timeout=600)
    outputsaver.save_output()
