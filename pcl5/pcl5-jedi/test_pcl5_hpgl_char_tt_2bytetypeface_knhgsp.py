import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using knhgsp.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:knhgsp.obj=9931406968b6ebb51b16c241aeff64fce1b36bfcd4d226cc9947cf5df9c7b90a
    +test_classification:System
    +name: test_pcl5_hpgl_char_tt_2bytetypeface_knhgsp
    +test:
        +title: test_pcl5_hpgl_char_tt_2bytetypeface_knhgsp
        +guid:538b3995-38c2-44cb-97f6-517ee4965507
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_tt_2bytetypeface_knhgsp(setup_teardown, printjob, outputsaver):
    printjob.print_verify('9931406968b6ebb51b16c241aeff64fce1b36bfcd4d226cc9947cf5df9c7b90a', timeout=600)
    outputsaver.save_output()
