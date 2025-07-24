import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:PCL5 high value test using **81037-50pgs_a4_Plain.prn
    +test_tier: 1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-156300
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:81037-50pgs_a4_Plain.prn=195a54f64f4aab5e7b6eb82f4181009d6a704dfe58e53b6e3350bcc91c438717
    +name:test_pcl5_conf_hv_81037_50pgs_a4_plain
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl5_conf_hv_81037_50pgs_a4_plain
        +guid:2db98a33-7ebb-481c-bbdd-efd2406c5bee
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_conf_hv_81037_50pgs_a4_plain(setup_teardown, printjob, outputverifier):
    printjob.print_verify('195a54f64f4aab5e7b6eb82f4181009d6a704dfe58e53b6e3350bcc91c438717', timeout=300)
    outputverifier.save_and_parse_output()
