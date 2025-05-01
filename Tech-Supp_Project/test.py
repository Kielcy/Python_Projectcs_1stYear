import os
import json
import datetime
import platform
import time
from getpass import getpass
import random

# ANSI Colors and formatting
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    @staticmethod
    def is_windows():
        return platform.system().lower() == "windows"
        
    @staticmethod
    def init():
        """Initialize colors for Windows"""
        if Colors.is_windows():
            os.system('color')
    
    @staticmethod
    def clear_screen():
        """Clear the console screen"""
        os.system('cls' if Colors.is_windows() else 'clear')


class LabAssist:
    def __init__(self):
        self.complaints = []
        # Default admin account for authentication
        self.admin_credentials = {"admin": "admin123"}
        self.common_issues = [
            "Computer not turning on",
            "Software not responding",
            "Printer not working",
            "Monitor display issues",
            "Internet connectivity problems",
            "Peripheral device issues",
            "Software installation problems",
            "Other"
        ]
        Colors.init()
        self.load_complaints()

    def load_complaints(self):
        """Load complaints from file if exists"""
        if os.path.exists("complaints.json"):
            try:
                with open("complaints.json", "r") as file:
                    self.complaints = json.load(file)
                    print(f"{Colors.GREEN}✓ Complaints loaded successfully{Colors.ENDC}")
            except:
                print(f"{Colors.RED}! Error loading complaints file. Starting with empty list.{Colors.ENDC}")
                self.complaints = []
        else:
            print(f"{Colors.YELLOW}ℹ No existing complaints file found. Starting fresh.{Colors.ENDC}")

    def save_complaints(self):
        """Save complaints to file"""
        try:
            with open("complaints.json", "w") as file:
                json.dump(self.complaints, file, indent=4)
            return True
        except Exception as e:
            print(f"{Colors.RED}! Error saving complaints: {str(e)}{Colors.ENDC}")
            return False

    def display_welcome(self):
        """Display welcome message"""
        Colors.clear_screen()
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        current_time = datetime.datetime.now().strftime("%H:%M")
        
        print(f"\n{Colors.BLUE}{Colors.BOLD}╔══════════════════════════════════════════════════════════╗{Colors.ENDC}")
        print(f"{Colors.BLUE}{Colors.BOLD}║                      LAB ASSIST                          ║{Colors.ENDC}")
        print(f"{Colors.BLUE}{Colors.BOLD}║              Laboratory Assistance System                ║{Colors.ENDC}")
        print(f"{Colors.BLUE}{Colors.BOLD}╚══════════════════════════════════════════════════════════╝{Colors.ENDC}")
        print(f"{Colors.CYAN}{current_date} | {current_time}{Colors.ENDC}")
        print(f"\n{Colors.YELLOW}Welcome to the laboratory support management system.{Colors.ENDC}")

    def get_role(self):
        """Prompt user to select role"""
        print(f"\n{Colors.BOLD}Please select your role:{Colors.ENDC}")
        print(f"  {Colors.CYAN}1.{Colors.ENDC} Student")
        print(f"  {Colors.CYAN}2.{Colors.ENDC} Admin")
        print(f"  {Colors.CYAN}3.{Colors.ENDC} Exit")
        
        while True:
            choice = input(f"\n{Colors.BOLD}Enter your choice (1-3):{Colors.ENDC} ")
            
            if choice == "1":
                return "student"
            elif choice == "2":
                return "admin"
            elif choice == "3":
                return "exit"
            else:
                print(f"{Colors.RED}! Invalid choice. Please try again.{Colors.ENDC}")

    def student_flow(self):
        """Handle student complaint submission"""
        Colors.clear_screen()
        print(f"\n{Colors.BLUE}{Colors.BOLD}╔══════════════════════════════════════════════════════════╗{Colors.ENDC}")
        print(f"{Colors.BLUE}{Colors.BOLD}║                  SUBMIT A LAB ISSUE                      ║{Colors.ENDC}")
        print(f"{Colors.BLUE}{Colors.BOLD}╚══════════════════════════════════════════════════════════╝{Colors.ENDC}")
        
        # Display list of common issues
        print(f"\n{Colors.BOLD}Common Lab Issues:{Colors.ENDC}")
        for i, issue in enumerate(self.common_issues, 1):
            print(f"  {Colors.CYAN}{i}.{Colors.ENDC} {issue}")
        
        # Prompt user to select issue
        while True:
            try:
                issue_choice = int(input(f"\n{Colors.BOLD}Select an issue (1-{len(self.common_issues)}):{Colors.ENDC} "))
                if 1 <= issue_choice <= len(self.common_issues):
                    selected_issue = self.common_issues[issue_choice - 1]
                    break
                else:
                    print(f"{Colors.RED}! Invalid choice. Please try again.{Colors.ENDC}")
            except ValueError:
                print(f"{Colors.RED}! Please enter a number.{Colors.ENDC}")
        
        # If "Other", prompt for description
        if selected_issue == "Other":
            issue_description = input(f"\n{Colors.BOLD}Please describe your issue:{Colors.ENDC} ")
        else:
            issue_description = selected_issue
        
        # Get PC number
        pc_number = input(f"\n{Colors.BOLD}Enter PC number:{Colors.ENDC} ")
        while not pc_number.strip():
            print(f"{Colors.RED}! PC number cannot be empty.{Colors.ENDC}")
            pc_number = input(f"{Colors.BOLD}Enter PC number:{Colors.ENDC} ")
        
        # Get room number
        room_number = input(f"\n{Colors.BOLD}Enter room number:{Colors.ENDC} ")
        while not room_number.strip():
            print(f"{Colors.RED}! Room number cannot be empty.{Colors.ENDC}")
            room_number = input(f"{Colors.BOLD}Enter room number:{Colors.ENDC} ")
        
        # Get student name
        student_name = input(f"\n{Colors.BOLD}Enter your name:{Colors.ENDC} ")
        while not student_name.strip():
            print(f"{Colors.RED}! Name cannot be empty.{Colors.ENDC}")
            student_name = input(f"{Colors.BOLD}Enter your name:{Colors.ENDC} ")
            
        additional_details = input(f"\n{Colors.BOLD}Any additional details (press Enter if none):{Colors.ENDC} ")
        
        # Handle troubleshooting for common issues
        resolved = False
        priority = "medium"  # Default priority
        
        if selected_issue != "Other":
            print(f"\n{Colors.GREEN}{Colors.BOLD}Troubleshooting suggestion for '{selected_issue}':{Colors.ENDC}")
            suggestion = self.get_troubleshooting_suggestion(selected_issue)
            print(f"{Colors.CYAN}{suggestion}{Colors.ENDC}")
            
            # Show troubleshooting animation
            print(f"\n{Colors.YELLOW}Analyzing possible solutions...{Colors.ENDC}")
            self.display_loading_animation(3)
            
            # Ask if suggestion worked
            while True:
                worked = input(f"\n{Colors.BOLD}Did the suggestion solve your problem? (yes/no):{Colors.ENDC} ").lower()
                if worked.startswith('y') or worked.startswith('n'):
                    resolved = worked.startswith('y')
                    break
                else:
                    print(f"{Colors.RED}! Please answer 'yes' or 'no'.{Colors.ENDC}")
            
            if resolved:
                print(f"\n{Colors.GREEN}✓ Great! Your issue has been marked as resolved.{Colors.ENDC}")
                priority = "low"
            else:
                print(f"\n{Colors.YELLOW}We're sorry to hear that.{Colors.ENDC}")
                # Ask if priority issue
                while True:
                    priority_choice = input(f"\n{Colors.BOLD}Is this a priority issue? (yes/no):{Colors.ENDC} ").lower()
                    if priority_choice.startswith('y') or priority_choice.startswith('n'):
                        priority = "high" if priority_choice.startswith('y') else "medium"
                        break
                    else:
                        print(f"{Colors.RED}! Please answer 'yes' or 'no'.{Colors.ENDC}")
        else:
            # For "Other" issues
            while True:
                priority_choice = input(f"\n{Colors.BOLD}Is this a priority issue? (yes/no):{Colors.ENDC} ").lower()
                if priority_choice.startswith('y') or priority_choice.startswith('n'):
                    priority = "high" if priority_choice.startswith('y') else "medium"
                    break
                else:
                    print(f"{Colors.RED}! Please answer 'yes' or 'no'.{Colors.ENDC}")
        
        # Create complaint
        new_id = 1
        if self.complaints:
            new_id = max(complaint['id'] for complaint in self.complaints) + 1
            
        complaint = {
            "id": new_id,
            "issue_type": selected_issue,
            "description": issue_description,
            "pc_number": pc_number,
            "room_number": room_number,
            "student_name": student_name,
            "additional_details": additional_details,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "resolved": resolved,
            "priority": priority
        }
        
        # Save complaint with loading animation
        print(f"\n{Colors.YELLOW}Registering your complaint...{Colors.ENDC}")
        self.display_loading_animation(2)
        self.complaints.append(complaint)
        saved = self.save_complaints()
        
        if saved:
            print(f"\n{Colors.GREEN}✓ Your complaint has been registered successfully!{Colors.ENDC}")
            
            # Display complaint receipt
            print(f"\n{Colors.BLUE}┌──────────────── COMPLAINT RECEIPT ────────────────┐{Colors.ENDC}")
            print(f"{Colors.BLUE}│{Colors.ENDC} {Colors.BOLD}Complaint ID:{Colors.ENDC} {complaint['id']:<36} {Colors.BLUE}│{Colors.ENDC}")
            print(f"{Colors.BLUE}│{Colors.ENDC} {Colors.BOLD}Issue:{Colors.ENDC} {complaint['issue_type']:<41} {Colors.BLUE}│{Colors.ENDC}")
            print(f"{Colors.BLUE}│{Colors.ENDC} {Colors.BOLD}PC Number:{Colors.ENDC} {complaint['pc_number']:<37} {Colors.BLUE}│{Colors.ENDC}")
            print(f"{Colors.BLUE}│{Colors.ENDC} {Colors.BOLD}Room Number:{Colors.ENDC} {complaint['room_number']:<35} {Colors.BLUE}│{Colors.ENDC}")
            print(f"{Colors.BLUE}│{Colors.ENDC} {Colors.BOLD}Student Name:{Colors.ENDC} {complaint['student_name']:<35} {Colors.BLUE}│{Colors.ENDC}")
            
            status_color = Colors.GREEN if complaint['resolved'] else Colors.YELLOW
            status_text = "Resolved" if complaint['resolved'] else "Unresolved"
            print(f"{Colors.BLUE}│{Colors.ENDC} {Colors.BOLD}Status:{Colors.ENDC} {status_color}{status_text}{Colors.ENDC}{' ' * (40 - len(status_text))} {Colors.BLUE}│{Colors.ENDC}")
            
            priority_color = Colors.RED if priority == "high" else (Colors.YELLOW if priority == "medium" else Colors.GREEN)
            print(f"{Colors.BLUE}│{Colors.ENDC} {Colors.BOLD}Priority:{Colors.ENDC} {priority_color}{priority.capitalize()}{Colors.ENDC}{' ' * (38 - len(priority))} {Colors.BLUE}│{Colors.ENDC}")
            print(f"{Colors.BLUE}└─────────────────────────────────────────────────────┘{Colors.ENDC}")
        else:
            print(f"\n{Colors.RED}! There was an error saving your complaint. Please try again later.{Colors.ENDC}")
        
        input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.ENDC}")

    def display_loading_animation(self, seconds):
        """Display a simple loading animation"""
        animations = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
        end_time = time.time() + seconds
        i = 0
        while time.time() < end_time:
            print(f"\r{Colors.CYAN}{animations[i % len(animations)]}{Colors.ENDC}", end='', flush=True)
            time.sleep(0.1)
            i += 1
        print("\r", end='', flush=True)

    def get_troubleshooting_suggestion(self, issue):
        """Return troubleshooting suggestion for common issues"""
        suggestions = {
            "Computer not turning on": "1. Check if the power cable is properly connected\n2. Ensure the power outlet is working\n3. Try pressing the power button for 10 seconds, then turn it on again",
            "Software not responding": "1. Try using Ctrl+Alt+Delete and open Task Manager\n2. End the non-responsive program\n3. Restart the software",
            "Printer not working": "1. Check if the printer is turned on and connected\n2. Verify paper and ink/toner levels\n3. Restart the printer and try again",
            "Monitor display issues": "1. Check if the monitor is properly connected to the PC\n2. Adjust brightness/contrast settings\n3. Try a different display cable",
            "Internet connectivity problems": "1. Check network cable connections\n2. Restart the computer\n3. Try disconnecting and reconnecting to the network",
            "Peripheral device issues": "1. Unplug and reconnect the device\n2. Try a different USB port\n3. Restart the computer",
            "Software installation problems": "1. Make sure you have administrator privileges\n2. Close all other applications before installing\n3. Try running the installer as administrator"
        }
        
        return suggestions.get(issue, "Please contact lab staff for assistance with this issue.")

    def admin_login(self):
        """Verify admin credentials"""
        Colors.clear_screen()
        print(f"\n{Colors.BLUE}{Colors.BOLD}╔══════════════════════════════════════════════════════════╗{Colors.ENDC}")
        print(f"{Colors.BLUE}{Colors.BOLD}║                     ADMIN LOGIN                          ║{Colors.ENDC}")
        print(f"{Colors.BLUE}{Colors.BOLD}╚══════════════════════════════════════════════════════════╝{Colors.ENDC}")
        
        attempts = 0
        max_attempts = 3
        
        while attempts < max_attempts:
            username = input(f"\n{Colors.BOLD}Username:{Colors.ENDC} ")
            password = getpass(f"{Colors.BOLD}Password:{Colors.ENDC} ")
            
            print(f"\n{Colors.YELLOW}Authenticating...{Colors.ENDC}")
            self.display_loading_animation(1)
            
            if username in self.admin_credentials and self.admin_credentials[username] == password:
                print(f"\n{Colors.GREEN}✓ Login successful!{Colors.ENDC}")
                return True
            else:
                attempts += 1
                remaining = max_attempts - attempts
                if remaining > 0:
                    print(f"\n{Colors.RED}! Invalid credentials. {remaining} attempts remaining.{Colors.ENDC}")
                else:
                    print(f"\n{Colors.RED}! Maximum login attempts reached. Access denied.{Colors.ENDC}")
            
        return False

    def admin_flow(self):
        """Handle admin functionality"""
        if not self.admin_login():
            input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.ENDC}")
            return
        
        while True:
            Colors.clear_screen()
            print(f"\n{Colors.BLUE}{Colors.BOLD}╔══════════════════════════════════════════════════════════╗{Colors.ENDC}")
            print(f"{Colors.BLUE}{Colors.BOLD}║                     ADMIN PANEL                          ║{Colors.ENDC}")
            print(f"{Colors.BLUE}{Colors.BOLD}╚══════════════════════════════════════════════════════════╝{Colors.ENDC}")
            
            # Show complaints stats summary
            total = len(self.complaints)
            resolved = len([c for c in self.complaints if c["resolved"]])
            unresolved = total - resolved
            high_priority = len([c for c in self.complaints if c["priority"] == "high" and not c["resolved"]])
            
            print(f"\n{Colors.BOLD}Dashboard Summary:{Colors.ENDC}")
            print(f"  {Colors.CYAN}Total Complaints:{Colors.ENDC} {total}")
            print(f"  {Colors.GREEN}Resolved:{Colors.ENDC} {resolved}")
            print(f"  {Colors.YELLOW}Unresolved:{Colors.ENDC} {unresolved}")
            print(f"  {Colors.RED}High Priority Unresolved:{Colors.ENDC} {high_priority}")
            
            print(f"\n{Colors.BOLD}Select an option:{Colors.ENDC}")
            print(f"  {Colors.CYAN}1.{Colors.ENDC} View Recent Complaints (Last 5)")
            print(f"  {Colors.CYAN}2.{Colors.ENDC} View All Complaints")
            print(f"  {Colors.CYAN}3.{Colors.ENDC} View Resolved Complaints")
            print(f"  {Colors.CYAN}4.{Colors.ENDC} View Unresolved Complaints")
            print(f"  {Colors.CYAN}5.{Colors.ENDC} Return to Main Menu")
            
            choice = input(f"\n{Colors.BOLD}Enter your choice (1-5):{Colors.ENDC} ")
            
            if choice == "1":
                self.view_complaints("recent")
            elif choice == "2":
                self.view_complaints("all")
            elif choice == "3":
                self.view_complaints("resolved")
            elif choice == "4":
                self.view_complaints("unresolved")
            elif choice == "5":
                break
            else:
                print(f"{Colors.RED}! Invalid choice. Please try again.{Colors.ENDC}")
                input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.ENDC}")

    def view_complaints(self, filter_type):
        """Display complaints based on filter"""
        Colors.clear_screen()
        filtered_complaints = []
        
        if filter_type == "recent":
            # Get the 5 most recent complaints
            filtered_complaints = sorted(self.complaints, key=lambda x: x["timestamp"], reverse=True)[:5]
            filter_title = "RECENT COMPLAINTS"
        elif filter_type == "all":
            filtered_complaints = self.complaints
            filter_title = "ALL COMPLAINTS"
        elif filter_type == "resolved":
            filtered_complaints = [c for c in self.complaints if c["resolved"]]
            filter_title = "RESOLVED COMPLAINTS"
        elif filter_type == "unresolved":
            filtered_complaints = [c for c in self.complaints if not c["resolved"]]
            filter_title = "UNRESOLVED COMPLAINTS"
        
        print(f"\n{Colors.BLUE}{Colors.BOLD}╔══════════════════════════════════════════════════════════╗{Colors.ENDC}")
        print(f"{Colors.BLUE}{Colors.BOLD}║ {filter_title.center(56)} ║{Colors.ENDC}")
        print(f"{Colors.BLUE}{Colors.BOLD}╚══════════════════════════════════════════════════════════╝{Colors.ENDC}")
        
        if not filtered_complaints:
            print(f"\n{Colors.YELLOW}ℹ No complaints found for this category.{Colors.ENDC}")
            input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.ENDC}")
            return
        
        # Display complaints summary
        print(f"\n{Colors.BOLD}{'ID':<5} {'Issue Type':<25} {'Priority':<10} {'Room':<8} {'Status':<12} {'Date':<19}{Colors.ENDC}")
        print(f"{Colors.BLUE}{'─' * 80}{Colors.ENDC}")
        
        for c in filtered_complaints:
            status = "Resolved" if c["resolved"] else "Unresolved"
            status_color = Colors.GREEN if c["resolved"] else Colors.YELLOW
            
            priority_color = Colors.RED if c["priority"] == "high" else (Colors.YELLOW if c["priority"] == "medium" else Colors.GREEN)
            
            print(f"{c['id']:<5} {c['issue_type'][:23]:<25} {priority_color}{c['priority']:<10}{Colors.ENDC} {c['room_number']:<8} {status_color}{status:<12}{Colors.ENDC} {c['timestamp']}")
        
        # Prompt admin to select a complaint
        while True:
            try:
                complaint_id = input(f"\n{Colors.BOLD}Enter complaint ID to view details (0 to go back):{Colors.ENDC} ")
                if complaint_id == '0':
                    return
                
                complaint_id = int(complaint_id)
                # Find selected complaint
                selected = next((c for c in self.complaints if c["id"] == complaint_id), None)
                
                if selected:
                    self.display_complaint_details(selected)
                    break
                else:
                    print(f"{Colors.RED}! Complaint not found. Please enter a valid ID.{Colors.ENDC}")
            except ValueError:
                print(f"{Colors.RED}! Please enter a valid complaint ID.{Colors.ENDC}")
        
        input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.ENDC}")

    def display_complaint_details(self, complaint):
        """Display detailed view of a complaint and allow status update"""
        Colors.clear_screen()
        print(f"\n{Colors.BLUE}{Colors.BOLD}╔══════════════════════════════════════════════════════════╗{Colors.ENDC}")
        print(f"{Colors.BLUE}{Colors.BOLD}║                 COMPLAINT DETAILS                        ║{Colors.ENDC}")
        print(f"{Colors.BLUE}{Colors.BOLD}╚══════════════════════════════════════════════════════════╝{Colors.ENDC}")
        
        status = "Resolved" if complaint['resolved'] else "Unresolved"
        status_color = Colors.GREEN if complaint['resolved'] else Colors.YELLOW
        
        priority_color = Colors.RED if complaint["priority"] == "high" else (Colors.YELLOW if complaint["priority"] == "medium" else Colors.GREEN)
        
        print(f"\n{Colors.BLUE}┌──────────────────────────────────────────────────────────┐{Colors.ENDC}")
        print(f"{Colors.BLUE}│{Colors.ENDC} {Colors.BOLD}ID:{Colors.ENDC} {complaint['id']:<54} {Colors.BLUE}│{Colors.ENDC}")
        print(f"{Colors.BLUE}│{Colors.ENDC} {Colors.BOLD}Issue Type:{Colors.ENDC} {complaint['issue_type']:<46} {Colors.BLUE}│{Colors.ENDC}")
        print(f"{Colors.BLUE}│{Colors.ENDC} {Colors.BOLD}Description:{Colors.ENDC} {complaint['description'][:45]:<44} {Colors.BLUE}│{Colors.ENDC}")
        print(f"{Colors.BLUE}│{Colors.ENDC} {Colors.BOLD}PC Number:{Colors.ENDC} {complaint['pc_number']:<46} {Colors.BLUE}│{Colors.ENDC}")
        print(f"{Colors.BLUE}│{Colors.ENDC} {Colors.BOLD}Room Number:{Colors.ENDC} {complaint['room_number']:<44} {Colors.BLUE}│{Colors.ENDC}")
        print(f"{Colors.BLUE}│{Colors.ENDC} {Colors.BOLD}Student Name:{Colors.ENDC} {complaint['student_name']:<44} {Colors.BLUE}│{Colors.ENDC}")
        
        add_details = complaint['additional_details'] if complaint['additional_details'] else 'None'
        print(f"{Colors.BLUE}│{Colors.ENDC} {Colors.BOLD}Additional Details:{Colors.ENDC} {add_details[:40]:<39} {Colors.BLUE}│{Colors.ENDC}")
        print(f"{Colors.BLUE}│{Colors.ENDC} {Colors.BOLD}Submitted:{Colors.ENDC} {complaint['timestamp']:<46} {Colors.BLUE}│{Colors.ENDC}")
        print(f"{Colors.BLUE}│{Colors.ENDC} {Colors.BOLD}Priority:{Colors.ENDC} {priority_color}{complaint['priority'].capitalize()}{Colors.ENDC}{' ' * (46 - len(complaint['priority']))} {Colors.BLUE}│{Colors.ENDC}")
        print(f"{Colors.BLUE}│{Colors.ENDC} {Colors.BOLD}Status:{Colors.ENDC} {status_color}{status}{Colors.ENDC}{' ' * (48 - len(status))} {Colors.BLUE}│{Colors.ENDC}")
        print(f"{Colors.BLUE}└──────────────────────────────────────────────────────────┘{Colors.ENDC}")
        
        # Prompt to update status
        print(f"\n{Colors.BOLD}Update status options:{Colors.ENDC}")
        print(f"  {Colors.GREEN}r{Colors.ENDC} - Mark as resolved")
        print(f"  {Colors.YELLOW}u{Colors.ENDC} - Mark as unresolved")
        print(f"  {Colors.CYAN}x{Colors.ENDC} - No change")
        
        while True:
            new_status = input(f"\n{Colors.BOLD}Update status (r/u/x):{Colors.ENDC} ").lower()
            
            if new_status == 'r':
                print(f"\n{Colors.YELLOW}Updating status...{Colors.ENDC}")
                self.display_loading_animation(1)
                complaint['resolved'] = True
                if self.save_complaints():
                    print(f"\n{Colors.GREEN}✓ Complaint marked as resolved.{Colors.ENDC}")
                else:
                    print(f"\n{Colors.RED}! Error updating status.{Colors.ENDC}")
                break
            elif new_status == 'u':
                print(f"\n{Colors.YELLOW}Updating status...{Colors.ENDC}")
                self.display_loading_animation(1)
                complaint['resolved'] = False
                if self.save_complaints():
                    print(f"\n{Colors.YELLOW}ℹ Complaint marked as unresolved.{Colors.ENDC}")
                else:
                    print(f"\n{Colors.RED}! Error updating status.{Colors.ENDC}")
                break
            elif new_status == 'x':
                print(f"\n{Colors.CYAN}ℹ Status unchanged.{Colors.ENDC}")
                break
            else:
                print(f"{Colors.RED}! Invalid choice. Please try again.{Colors.ENDC}")

    def run(self):
        """Main application loop"""
        self.display_welcome()
        
        while True:
            role = self.get_role()
            
            if role == "student":
                self.student_flow()
                Colors.clear_screen()
                self.display_welcome()
            elif role == "admin":
                self.admin_flow()
                Colors.clear_screen()
                self.display_welcome()
            elif role == "exit":
                Colors.clear_screen()
                print(f"\n{Colors.GREEN}{Colors.BOLD}Thank You for Using LabAssist! We appreciate your trust in LabAssist to support your laboratory needs. Your efficiency and accuracy are our top priorities, and we’re here to help every step of the way. If you have any feedback or need assistance, don’t hesitate to reach out. See you next time!{Colors.ENDC}")
                break


if __name__ == "__main__":
    app = LabAssist()
    app.run()
