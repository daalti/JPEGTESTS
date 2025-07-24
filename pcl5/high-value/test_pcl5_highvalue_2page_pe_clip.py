import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 2Page_pe_clip.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:2Page-pe_clip.obj=a445c7bf4f110da85bf09508cc8a610ee597194c3a8557fe1c3d91bf8d2b92f9
    +test_classification:System
    +name: test_pcl5_highvalue_2page_pe_clip
    +test:
        +title: test_pcl5_highvalue_2page_pe_clip
        +guid:9a26e510-60b6-4efb-a7b6-b7e70e064507
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

def test_pcl5_highvalue_2page_pe_clip(setup_teardown, printjob, outputsaver):
    printjob.print_verify('a445c7bf4f110da85bf09508cc8a610ee597194c3a8557fe1c3d91bf8d2b92f9', timeout=600)
    outputsaver.save_output()
