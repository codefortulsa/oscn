import oscn

class TestCaseDateFinders:

    def test_filed_date(self):
        # Set the HTML response containing the 'Filed' date
        html = """
        <td valign="center" width="50%">WEBB, JON et al VS. CUPPS, GARY B et al</td>
        <td width="50%"><strong>
                No. CJ-2022-00141<br>
                (Civil relief more than $10,000: JUDGMENT (DISMISSED))
              </strong><br><br>
              Filed: 05/31/2022<br><br><br>Judge: PARISH, LAWRENCE<br></td>
        """
        case = oscn.request.Case(text=html)  # Setting the HTML text during instantiation
        filed_date = case.filed
        assert filed_date == "05/31/2022"

    def test_closed_date(self):
        # Set the HTML response containing the 'Closed' date
        html = """
        <strong>
                No. CM-2022-141<br>
                (Criminal Misdemeanor)
              </strong><br><br>
              Filed: 01/13/2022<br>Closed: 03/09/2022<br><br>Judge: Traffic Court Judge (General)<br>
        """
        case = oscn.request.Case(text=html)  # Setting the HTML text during instantiation
        closed_date = case.closed
        assert closed_date == "03/09/2022"

    def test_offense_date(self):
        # Set the HTML response containing the 'Date of Offense'
        html = """
        Count as Filed: 
        LA4, POSSESSION OF STOLEN VEHICLE, 
        in violation of <a href="http://www.oscn.net/applications/oscn/deliverdocument.asp?box1=47&amp;box2=OS&amp;box3=4-103">47 O.S. 4-103</a><br>Date of Offense: 01/07/2022<br>
        """
        case = oscn.request.Case(text=html)  # Setting the HTML text during instantiation
        offense_date = case.offense
        assert offense_date == "01/07/2022"
