import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 74Page_udssdown.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:1020
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:74Page-udssdown.obj=530d32f2b529d3e8a0913e8d0be4eaf1ac92cbc80532c4bfc39d50b5ee92e35b
    +test_classification:System
    +name: test_pcl5_highvalue_74page_udssdown
    +test:
        +title: test_pcl5_highvalue_74page_udssdown
        +guid:900508a2-76e6-49b5-868e-44694e905eb8
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

def test_pcl5_highvalue_74page_udssdown(setup_teardown, printjob, outputsaver):
    printjob.print_verify('530d32f2b529d3e8a0913e8d0be4eaf1ac92cbc80532c4bfc39d50b5ee92e35b', timeout=900)
    outputsaver.save_output()
