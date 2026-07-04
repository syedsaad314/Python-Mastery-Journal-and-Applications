# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Term Validation Mechanics
Description: Forces active leaders or candidates to immediately stand down 
             if they encounter a message containing a higher logical term.
"""
class TermSanitizationLayer:
    def __init__(self, term: int, is_leader: bool) -> None:
        self.current_term = term
        self.is_leader = is_leader

    def process_incoming_metadata(self, inbound_term: int) -> bool:
        if inbound_term > self.current_term:
            self.current_term = inbound_term
            self.is_leader = False # Revert to follower status
            return True
        return False

if __name__ == "__main__":
    layer = TermSanitizationLayer(term=5, is_leader=True)
    stepped_down = layer.process_incoming_metadata(inbound_term=6)
    assert stepped_down == True
    assert layer.is_leader == False
    assert layer.current_term == 6