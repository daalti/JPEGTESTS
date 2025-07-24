import pytest
import logging

from dunetuf.print.output.intents import Intents


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:PCL5 high value test using **80583-5pgs10mop_Letter_STPL-ONE_STAPLE_jlB1.prn
    +test_tier: 1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-156300
    +timeout:420
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:80583-5pgs10mop_Letter_STPL-ONE_STAPLE_jlB1.prn=e86fdc150a7279d5c4166b79f8daf17d432ec32dbea49ecabb8417fd747b543d
    +name:test_pcl5_conf_hv_80583_5pgs10mop_letter_stpl_one_staple_jlb1
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl5_conf_hv_80583_5pgs10mop_letter_stpl_one_staple_jlb1
        +guid:1f784227-1eb5-4a1d-9e96-4a3570a91390
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_conf_hv_80583_5pgs10mop_letter_stpl_one_staple_jlb1(setup_teardown, printjob, outputverifier):
    printjob.print_verify('e86fdc150a7279d5c4166b79f8daf17d432ec32dbea49ecabb8417fd747b543d', timeout=300)
    outputverifier.save_and_parse_output()
