from scripts import permit_reader


def test_date_parse():

    dt = permit_reader.date_parse('1/2/2008')
    assert dt.month == 1
    assert dt.day == 2
    assert dt.year == 2008

    dt = permit_reader.date_parse('22-FEB-02')
    assert dt.month == 2
    assert dt.day == 22
    assert dt.year == 2002
