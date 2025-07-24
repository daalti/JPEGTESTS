import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 67Page_enhlogop.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:900
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:67Page-enhlogop.obj=1afc44555b5c15a5f45d0193cede0efe0e60d6dc40a0d565b683fa01676e291d
    +test_classification:System
    +name: test_pcl5_highvalue_67page_enhlogop
    +test:
        +title: test_pcl5_highvalue_67page_enhlogop
        +guid:06465b36-cad2-486f-bb0c-fddc7aa9cee0
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

def test_pcl5_highvalue_67page_enhlogop(setup_teardown, printjob, counters, outputsaver):
    printjob.print_verify('1afc44555b5c15a5f45d0193cede0efe0e60d6dc40a0d565b683fa01676e291d', timeout=900)
    outputsaver.save_output()
