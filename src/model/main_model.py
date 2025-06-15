
class MainModel:
    def __init__(self):
        self.card_result = {}
        self.current_page = 0
        self.cards_per_page = 6

    def set_card_result(self, card_result):
        self.card_result = card_result
        
    def get_card_result_for_current_page(self):
        """Get candidates for current page"""
        start = self.current_page * self.cards_per_page
        end = min(start + self.cards_per_page, len(self.card_result))
        result = list(self.card_result.values())[start:end]
        print(f"model result: {result}")
        return result

    def get_total_pages(self):
        """Get total number of pages"""
        return (len(self.card_result) + self.cards_per_page - 1) // self.cards_per_page

    def can_go_previous(self):
        """Check if can go to previous page"""
        return self.current_page > 0
    
    def can_go_next(self):
        """Check if can go to next page"""
        return self.current_page < self.get_total_pages() - 1
    
    def go_previous_page(self):
        """Go to previous page"""
        if self.can_go_previous():
            self.current_page -= 1
            return True
        return False
    
    def go_next_page(self):
        """Go to next page"""
        if self.can_go_next():
            self.current_page += 1
            return True
        return False
    


