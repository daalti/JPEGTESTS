import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 38Page_dv2.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:38Page-dv2.obj=909543ccb8ae7ddcc55526976c1fdae2128c9caee969051bbf17049a7555c13c
    +test_classification:System
    +name: test_pcl5_highvalue_38page_dv2
    +test:
        +title: test_pcl5_highvalue_38page_dv2
        +guid:720562fb-8785-4344-9efb-91f4da207f3f
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

def test_pcl5_highvalue_38page_dv2(setup_teardown, printjob, outputsaver):
    printjob.print_verify('909543ccb8ae7ddcc55526976c1fdae2128c9caee969051bbf17049a7555c13c', timeout=600)
    outputsaver.save_output()
