import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 2Page_sa_tt.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:2Page-sa_tt.obj=2a8cae0b3596e642496fda3fec72c3fecff761438cf720dd739ed87a8897a308
    +test_classification:System
    +name: test_pcl5_highvalue_2page_sa_tt
    +test:
        +title: test_pcl5_highvalue_2page_sa_tt
        +guid:648b3411-2594-42d2-a9ed-e500d2149edb
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

def test_pcl5_highvalue_2page_sa_tt(setup_teardown, printjob, outputsaver):
    printjob.print_verify('2a8cae0b3596e642496fda3fec72c3fecff761438cf720dd739ed87a8897a308', timeout=600)
    outputsaver.save_output()
