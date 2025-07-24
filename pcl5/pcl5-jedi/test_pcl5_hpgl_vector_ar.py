import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using ar.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ar.obj=bd038fbfa896fb6d84e1fc948124dcc5bccef6ca989b6e5328eb212129a1ee41
    +test_classification:System
    +name: test_pcl5_hpgl_vector_ar
    +test:
        +title: test_pcl5_hpgl_vector_ar
        +guid:92d4aa85-c9cf-4bd1-b085-41124b1fb8bb
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_vector_ar(setup_teardown, printjob, outputsaver):
    printjob.print_verify('bd038fbfa896fb6d84e1fc948124dcc5bccef6ca989b6e5328eb212129a1ee41', timeout=600)
    outputsaver.save_output()
