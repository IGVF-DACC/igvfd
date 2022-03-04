def test_lab_title(lab, other_lab):
    assert(lab['title']) == 'Principal Investigator, Stanford'
    assert(other_lab['title']) == 'IGVF VerifiedMember, Other Institute'