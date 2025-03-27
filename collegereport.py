import datetime
import csv
import json
from fpdf import FPDF
import matplotlib.pyplot as plt
import pandas as pd

class EventReportGenerator:
    def __init__(self, event_name, event_date, organizer):
        self.event_name = event_name
        self.event_date = event_date
        self.organizer = organizer
        self.attendees = []
        self.feedback = []
        self.expenses = []
        self.sponsors = []
        self.activities = []

    def add_attendee(self, name, department, email):
        """Add an attendee to the event"""
        self.attendees.append({
            'name': name,
            'department': department,
            'email': email
        })

    def add_feedback(self, attendee_name, rating, comments):
        """Add feedback for the event"""
        self.feedback.append({
            'attendee_name': attendee_name,
            'rating': rating,
            'comments': comments,
            'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    def add_expense(self, item, amount, category):
        """Add an expense for the event"""
        self.expenses.append({
            'item': item,
            'amount': float(amount),
            'category': category
        })

    def add_sponsor(self, name, contribution, contact):
        """Add a sponsor for the event"""
        self.sponsors.append({
            'name': name,
            'contribution': contribution,
            'contact': contact
        })

    def add_activity(self, name, duration, responsible):
        """Add an activity to the event"""
        self.activities.append({
            'name': name,
            'duration': duration,
            'responsible': responsible
        })

    def generate_text_report(self):
        """Generate a text format report"""
        report = f"College Event Report\n{'='*50}\n\n"
        report += f"Event Name: {self.event_name}\n"
        report += f"Date: {self.event_date}\n"
        report += f"Organizer: {self.organizer}\n\n"

        report += f"Attendees ({len(self.attendees)}):\n"
        for attendee in self.attendees:
            report += f"- {attendee['name']} ({attendee['department']}, {attendee['email']})\n"

        report += f"\nActivities:\n"
        for activity in self.activities:
            report += f"- {activity['name']} ({activity['duration']}), Responsible: {activity['responsible']}\n"

        report += f"\nSponsors ({len(self.sponsors)}):\n"
        for sponsor in self.sponsors:
            report += f"- {sponsor['name']} (Contribution: {sponsor['contribution']}, Contact: {sponsor['contact']})\n"

        total_expenses = sum(expense['amount'] for expense in self.expenses)
        report += f"\nExpenses (Total: ${total_expenses:.2f}):\n"
        for expense in self.expenses:
            report += f"- {expense['item']}: ${expense['amount']:.2f} ({expense['category']})\n"

        if self.feedback:
            avg_rating = sum(fb['rating'] for fb in self.feedback) / len(self.feedback)
            report += f"\nFeedback (Average Rating: {avg_rating:.1f}/5):\n"
            for fb in self.feedback:
                report += f"- {fb['attendee_name']}: {fb['rating']}/5 - \"{fb['comments']}\"\n"

        return report

    def generate_pdf_report(self, filename):
        """Generate a PDF format report"""
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Title
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="College Event Report", ln=1, align='C')
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="="*50, ln=1, align='C')

        # Event details
        pdf.cell(200, 10, txt=f"Event Name: {self.event_name}", ln=1)
        pdf.cell(200, 10, txt=f"Date: {self.event_date}", ln=1)
        pdf.cell(200, 10, txt=f"Organizer: {self.organizer}", ln=1)
        pdf.ln(10)

        # Attendees
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt=f"Attendees ({len(self.attendees)}):", ln=1)
        pdf.set_font("Arial", size=12)
        for attendee in self.attendees:
            pdf.cell(200, 10, txt=f"- {attendee['name']} ({attendee['department']}, {attendee['email']})", ln=1)
        pdf.ln(5)

        # Activities
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt="Activities:", ln=1)
        pdf.set_font("Arial", size=12)
        for activity in self.activities:
            pdf.cell(200, 10, txt=f"- {activity['name']} ({activity['duration']}), Responsible: {activity['responsible']}", ln=1)
        pdf.ln(5)

        # Sponsors
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt=f"Sponsors ({len(self.sponsors)}):", ln=1)
        pdf.set_font("Arial", size=12)
        for sponsor in self.sponsors:
            pdf.cell(200, 10, txt=f"- {sponsor['name']} (Contribution: {sponsor['contribution']}, Contact: {sponsor['contact']})", ln=1)
        pdf.ln(5)

        # Expenses
        total_expenses = sum(expense['amount'] for expense in self.expenses)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt=f"Expenses (Total: ${total_expenses:.2f}):", ln=1)
        pdf.set_font("Arial", size=12)
        for expense in self.expenses:
            pdf.cell(200, 10, txt=f"- {expense['item']}: ${expense['amount']:.2f} ({expense['category']})", ln=1)
        pdf.ln(5)

        # Feedback
        if self.feedback:
            avg_rating = sum(fb['rating'] for fb in self.feedback) / len(self.feedback)
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(200, 10, txt=f"Feedback (Average Rating: {avg_rating:.1f}/5):", ln=1)
            pdf.set_font("Arial", size=12)
            for fb in self.feedback:
                pdf.multi_cell(0, 10, txt=f"- {fb['attendee_name']}: {fb['rating']}/5 - \"{fb['comments']}\"")

        # Save the PDF
        pdf.output(filename)

    def generate_csv_report(self, filename):
        """Generate CSV files for different aspects of the event"""
        # Attendees CSV
        with open(f'attendees_{filename}', 'w', newline='') as csvfile:
            fieldnames = ['name', 'department', 'email']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.attendees)

        # Expenses CSV
        with open(f'expenses_{filename}', 'w', newline='') as csvfile:
            fieldnames = ['item', 'amount', 'category']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.expenses)

        # Feedback CSV
        if self.feedback:
            with open(f'feedback_{filename}', 'w', newline='') as csvfile:
                fieldnames = ['attendee_name', 'rating', 'comments', 'timestamp']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.feedback)

    def generate_json_report(self, filename):
        """Generate a JSON format report"""
        report_data = {
            'event_name': self.event_name,
            'event_date': self.event_date,
            'organizer': self.organizer,
            'attendees': self.attendees,
            'activities': self.activities,
            'sponsors': self.sponsors,
            'expenses': self.expenses,
            'feedback': self.feedback
        }

        with open(filename, 'w') as jsonfile:
            json.dump(report_data, jsonfile, indent=4)

    def generate_visualizations(self, filename_prefix):
        """Generate visualizations for the event data"""
        if not self.feedback:
            return

        # Feedback ratings histogram
        ratings = [fb['rating'] for fb in self.feedback]
        plt.figure(figsize=(8, 6))
        plt.hist(ratings, bins=5, range=(1, 6), edgecolor='black')
        plt.title('Feedback Ratings Distribution')
        plt.xlabel('Rating (1-5)')
        plt.ylabel('Number of Responses')
        plt.savefig(f'{filename_prefix}_ratings.png')
        plt.close()

        # Expenses by category pie chart
        if self.expenses:
            df = pd.DataFrame(self.expenses)
            expenses_by_category = df.groupby('category')['amount'].sum()
            plt.figure(figsize=(8, 8))
            expenses_by_category.plot.pie(autopct='%1.1f%%')
            plt.title('Expenses by Category')
            plt.ylabel('')
            plt.savefig(f'{filename_prefix}_expenses.png')
            plt.close()

    def generate_full_report(self, filename_prefix):
        """Generate all report formats and visualizations"""
        # Generate text report
        text_report = self.generate_text_report()
        with open(f'{filename_prefix}.txt', 'w') as f:
            f.write(text_report)

        # Generate PDF report
        self.generate_pdf_report(f'{filename_prefix}.pdf')

        # Generate CSV reports
        self.generate_csv_report(f'{filename_prefix}.csv')

        # Generate JSON report
        self.generate_json_report(f'{filename_prefix}.json')

        # Generate visualizations
        self.generate_visualizations(filename_prefix)


# Example usage
if __name__ == "__main__":
    # Create an event report
    report = EventReportGenerator(
        event_name="Annual Tech Fest 2023",
        event_date="2023-11-15",
        organizer="Computer Science Department"
    )

    # Add attendees
    report.add_attendee("John Doe", "Computer Science", "john@college.edu")
    report.add_attendee("Jane Smith", "Electrical Engineering", "jane@college.edu")
    report.add_attendee("Bob Johnson", "Mechanical Engineering", "bob@college.edu")

    # Add activities
    report.add_activity("Hackathon", "4 hours", "Prof. Smith")
    report.add_activity("Robotics Workshop", "2 hours", "Dr. Brown")
    report.add_activity("AI Seminar", "1.5 hours", "Dr. Lee")

    # Add sponsors
    report.add_sponsor("Tech Corp", "$2000", "contact@techcorp.com")
    report.add_sponsor("Innovate Inc", "$1500", "support@innovate.com")

    # Add expenses
    report.add_expense("Venue Rental", 1000, "Venue")
    report.add_expense("Food and Beverages", 500, "Food")
    report.add_expense("Prizes", 800, "Awards")
    report.add_expense("Marketing Materials", 300, "Marketing")

    # Add feedback
    report.add_feedback("John Doe", 4, "Great event, especially enjoyed the hackathon!")
    report.add_feedback("Jane Smith", 5, "Excellent workshops, very informative.")
    report.add_feedback("Bob Johnson", 3, "Good overall, but some sessions ran too long.")

    # Generate all reports
    report.generate_full_report("tech_fest_2023_report")