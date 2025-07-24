import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using schss.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:schss.obj=fbb572d2fa7d28674b67ed963747bc92c0978adf4fb788fbff902a45b7927fed
    +test_classification:System
    +name: test_pcl5_hpgl_char_tt_2bytetypeface_schss
    +test:
        +title: test_pcl5_hpgl_char_tt_2bytetypeface_schss
        +guid:bf54c0b3-ccdc-4cf3-a3e3-3d8a931e4d0d
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_tt_2bytetypeface_schss(setup_teardown, printjob, outputsaver):
    printjob.print_verify('fbb572d2fa7d28674b67ed963747bc92c0978adf4fb788fbff902a45b7927fed', timeout=600)
    outputsaver.save_output()
