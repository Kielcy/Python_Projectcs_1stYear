import os
import json
import datetime
import platform
import time
from getpass import getpass
import heapq  # Import heapq for priority queue functionality

# ANSI Colors and formatting - Reduced to 3 colors only
class Colors:
    # Main three colors
    PRIMARY = '\033[94m'    # Blue - for headers and UI elements
    SECONDARY = '\033[96m'  # Cyan - for secondary elements
    SUCCESS = '\033[92m'    # Green - for success messages and positive status
    WARNING = '\033[91m'    # Red - for warnings, errors, and important notices
    
    # Basic formatting
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    
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


class PriorityQueue:
    """Priority Queue implementation for complaint management"""
    
    def __init__(self):
        self.queue = []
        self.entry_count = 0  # For tie-breaking when priorities are equal
    
    def push(self, complaint):
        """
        Add complaint to priority queue
        Priority order: 1 (high) -> 2 (low)
        """
        # Convert priority string to numeric value (lower is higher priority)
        priority_value = 1 if complaint['priority'] == "high" else 2
        
        # Push to heap with priority, unique count for stable sorting, and the complaint
        heapq.heappush(self.queue, (priority_value, self.entry_count, complaint))
        self.entry_count += 1
    
    def get_all_sorted(self):
        """Return all complaints sorted by priority without emptying the queue"""
        # Create a copy of the queue to avoid modifying the original
        queue_copy = self.queue.copy()
        result = []
        
        # Pop all items from the copy to get them in priority order
        while queue_copy:
            _, _, complaint = heapq.heappop(queue_copy)
            result.append(complaint)
            
        return result
    
    def clear(self):
        """Clear the priority queue"""
        self.queue = []
        self.entry_count = 0


class LabAssist:
    def __init__(self):
        self.complaints = []
        self.priority_queue = PriorityQueue()  # Initialize priority queue
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
        self.load_admin_credentials()  # Load admin credentials from file

    def load_complaints(self):
        """Load complaints from file if exists"""
        if os.path.exists("complaints.json"):
            try:
                with open("complaints.json", "r") as file:
                    self.complaints = json.load(file)
                    print(f"{Colors.SUCCESS}✓ Complaints loaded successfully{Colors.ENDC}")
                    
                    # Initialize priority queue with loaded complaints
                    self.update_priority_queue()
            except Exception as e:
                print(f"{Colors.WARNING}! Error loading complaints file: {str(e)}. Starting with empty list.{Colors.ENDC}")
                self.complaints = []
        else:
            print(f"{Colors.WARNING}ℹ No existing complaints file found. Starting fresh.{Colors.ENDC}")
    
    def load_admin_credentials(self):
        """Load admin credentials from file if exists"""
        if os.path.exists("admin_credentials.json"):
            try:
                with open("admin_credentials.json", "r") as file:
                    loaded_credentials = json.load(file)
                    
                    # Merge with default credentials, preserving default if not in file
                    self.admin_credentials.update(loaded_credentials)
                    
                    print(f"{Colors.SUCCESS}✓ Admin credentials loaded successfully{Colors.ENDC}")
            except Exception as e:
                print(f"{Colors.WARNING}! Error loading admin credentials: {str(e)}. Using default admin.{Colors.ENDC}")
        else:
            print(f"{Colors.WARNING}ℹ No existing admin credentials file found. Using default admin.{Colors.ENDC}")
    
    def update_priority_queue(self):
        """Update priority queue with current complaints"""
        self.priority_queue.clear()
        for complaint in self.complaints:
            self.priority_queue.push(complaint)

    def save_complaints(self):
        """Save complaints to file"""
        try:
            with open("complaints.json", "w") as file:
                json.dump(self.complaints, file, indent=4)
            # Update priority queue after saving
            self.update_priority_queue()
            return True
        except Exception as e:
            print(f"{Colors.WARNING}! Error saving complaints: {str(e)}{Colors.ENDC}")
            return False

    def save_admin_credentials(self):
        """Save admin credentials to file"""
        try:
            with open("admin_credentials.json", "w") as file:
                json.dump(self.admin_credentials, file, indent=4)
            return True
        except Exception as e:
            print(f"{Colors.WARNING}! Error saving admin credentials: {str(e)}{Colors.ENDC}")
            return False

    def display_welcome(self):
        """Display welcome message"""
        Colors.clear_screen()
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        current_time = datetime.datetime.now().strftime("%H:%M")
        
        print(f"\n{Colors.PRIMARY}{Colors.BOLD}╔══════════════════════════════════════════════════════════╗{Colors.ENDC}")
        print(f"{Colors.PRIMARY}{Colors.BOLD}║                      LAB ASSIST                          ║{Colors.ENDC}")
        print(f"{Colors.PRIMARY}{Colors.BOLD}║              Laboratory Assistance System                ║{Colors.ENDC}")
        print(f"{Colors.PRIMARY}{Colors.BOLD}╚══════════════════════════════════════════════════════════╝{Colors.ENDC}")
        print(f"{Colors.PRIMARY}{current_date} | {current_time}{Colors.ENDC}")
        print(f"\n{Colors.PRIMARY}Welcome to the laboratory support management system.{Colors.ENDC}")

    def get_role(self):
        """Prompt user to select role"""
        print(f"\n{Colors.BOLD}Please select your role:{Colors.ENDC}")
        print(f"  {Colors.PRIMARY}1.{Colors.ENDC} Student")
        print(f"  {Colors.PRIMARY}2.{Colors.ENDC} Admin")
        print(f"  {Colors.PRIMARY}3.{Colors.ENDC} Register New Admin")
        print(f"  {Colors.PRIMARY}4.{Colors.ENDC} Exit")
        
        while True:
            choice = input(f"\n{Colors.BOLD}Enter your choice (1-4):{Colors.ENDC} ")
            
            if choice == "1":
                return "student"
            elif choice == "2":
                return "admin"
            elif choice == "3":
                return "register"
            elif choice == "4":
                return "exit"
            else:
                print(f"{Colors.WARNING}! Invalid choice. Please try again.{Colors.ENDC}")

    def student_flow(self):
        """Handle student complaint submission"""
        Colors.clear_screen()
        print(f"\n{Colors.PRIMARY}{Colors.BOLD}╔══════════════════════════════════════════════════════════╗{Colors.ENDC}")
        print(f"{Colors.PRIMARY}{Colors.BOLD}║                  SUBMIT A LAB ISSUE                      ║{Colors.ENDC}")
        print(f"{Colors.PRIMARY}{Colors.BOLD}╚══════════════════════════════════════════════════════════╝{Colors.ENDC}")
        
        # Display list of common issues
        print(f"\n{Colors.BOLD}Common Lab Issues:{Colors.ENDC}")
        for i, issue in enumerate(self.common_issues, 1):
            print(f"  {Colors.PRIMARY}{i}.{Colors.ENDC} {issue}")
        
        # Prompt user to select issue
        while True:
            try:
                issue_choice = int(input(f"\n{Colors.BOLD}Select an issue (1-{len(self.common_issues)}):{Colors.ENDC} "))
                if 1 <= issue_choice <= len(self.common_issues):
                    selected_issue = self.common_issues[issue_choice - 1]
                    break
                else:
                    print(f"{Colors.WARNING}! Invalid choice. Please try again.{Colors.ENDC}")
            except ValueError:
                print(f"{Colors.WARNING}! Please enter a number.{Colors.ENDC}")
        
        # If "Other", prompt for description
        if selected_issue == "Other":
            issue_description = input(f"\n{Colors.BOLD}Please describe your issue:{Colors.ENDC} ")
        else:
            issue_description = selected_issue
        
        # Get PC number
        pc_number = input(f"\n{Colors.BOLD}Enter PC number:{Colors.ENDC} ")
        while not pc_number.strip():
            print(f"{Colors.WARNING}! PC number cannot be empty.{Colors.ENDC}")
            pc_number = input(f"{Colors.BOLD}Enter PC number:{Colors.ENDC} ")
        
        # Get room number
        room_number = input(f"\n{Colors.BOLD}Enter room number:{Colors.ENDC} ")
        while not room_number.strip():
            print(f"{Colors.WARNING}! Room number cannot be empty.{Colors.ENDC}")
            room_number = input(f"{Colors.BOLD}Enter room number:{Colors.ENDC} ")
        
        # Get student name
        student_name = input(f"\n{Colors.BOLD}Enter your name:{Colors.ENDC} ")
        while not student_name.strip():
            print(f"{Colors.WARNING}! Name cannot be empty.{Colors.ENDC}")
            student_name = input(f"{Colors.BOLD}Enter your name:{Colors.ENDC} ")
            
        additional_details = input(f"\n{Colors.BOLD}Any additional details (press Enter if none):{Colors.ENDC} ")
        
        # Handle troubleshooting for common issues
        resolved = False
        
        if selected_issue != "Other":
            print(f"\n{Colors.SUCCESS}{Colors.BOLD}Troubleshooting suggestion for '{selected_issue}':{Colors.ENDC}")
            suggestion = self.get_troubleshooting_suggestion(selected_issue)
            print(f"{Colors.PRIMARY}{suggestion}{Colors.ENDC}")
            
            # Show troubleshooting animation
            print(f"\n{Colors.PRIMARY}Analyzing possible solutions...{Colors.ENDC}")
            self.display_loading_animation(3)
            
            # Ask if suggestion worked
            while True:
                worked = input(f"\n{Colors.BOLD}Did the suggestion solve your problem? (yes/no):{Colors.ENDC} ").lower()
                if worked.startswith('y') or worked.startswith('n'):
                    resolved = worked.startswith('y')
                    break
                else:
                    print(f"{Colors.WARNING}! Please answer 'yes' or 'no'.{Colors.ENDC}")
            
            if resolved:
                print(f"\n{Colors.SUCCESS}✓ Great! Your issue has been marked as resolved.{Colors.ENDC}")
        
        # Set priority based on resolution status (simplified)
        priority = "low" if resolved else "high"
        
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
        print(f"\n{Colors.PRIMARY}Registering your complaint...{Colors.ENDC}")
        self.display_loading_animation(2)
        self.complaints.append(complaint)
        saved = self.save_complaints()
        
        if saved:
            print(f"\n{Colors.SUCCESS}✓ Your complaint has been registered successfully!{Colors.ENDC}")
            
            # Display complaint receipt
            print(f"\n{Colors.PRIMARY}┌──────────────── COMPLAINT RECEIPT ────────────────┐{Colors.ENDC}")
            print(f"{Colors.PRIMARY}│{Colors.ENDC} {Colors.BOLD}Complaint ID:{Colors.ENDC} {complaint['id']:<36} {Colors.PRIMARY}│{Colors.ENDC}")
            print(f"{Colors.PRIMARY}│{Colors.ENDC} {Colors.BOLD}Issue:{Colors.ENDC} {complaint['issue_type']:<41} {Colors.PRIMARY}│{Colors.ENDC}")
            print(f"{Colors.PRIMARY}│{Colors.ENDC} {Colors.BOLD}PC Number:{Colors.ENDC} {complaint['pc_number']:<37} {Colors.PRIMARY}│{Colors.ENDC}")
            print(f"{Colors.PRIMARY}│{Colors.ENDC} {Colors.BOLD}Room Number:{Colors.ENDC} {complaint['room_number']:<35} {Colors.PRIMARY}│{Colors.ENDC}")
            print(f"{Colors.PRIMARY}│{Colors.ENDC} {Colors.BOLD}Student Name:{Colors.ENDC} {complaint['student_name']:<35} {Colors.PRIMARY}│{Colors.ENDC}")
            
            status_color = Colors.SUCCESS if complaint['resolved'] else Colors.WARNING
            status_text = "Resolved" if complaint['resolved'] else "Unresolved"
            print(f"{Colors.PRIMARY}│{Colors.ENDC} {Colors.BOLD}Status:{Colors.ENDC} {status_color}{status_text}{Colors.ENDC}{' ' * (40 - len(status_text))} {Colors.PRIMARY}│{Colors.ENDC}")
            
            priority_color = Colors.WARNING if priority == "high" else Colors.SUCCESS
            print(f"{Colors.PRIMARY}│{Colors.ENDC} {Colors.BOLD}Priority:{Colors.ENDC} {priority_color}{priority.capitalize()}{Colors.ENDC}{' ' * (38 - len(priority))} {Colors.PRIMARY}│{Colors.ENDC}")
            print(f"{Colors.PRIMARY}└─────────────────────────────────────────────────────┘{Colors.ENDC}")
        else:
            print(f"\n{Colors.WARNING}! There was an error saving your complaint. Please try again later.{Colors.ENDC}")
        
        input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.ENDC}")

    def display_loading_animation(self, seconds):
        """Display a simple loading animation"""
        animations = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
        end_time = time.time() + seconds
        i = 0
        while time.time() < end_time:
            print(f"\r{Colors.PRIMARY}{animations[i % len(animations)]}{Colors.ENDC}", end='', flush=True)
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

    def register_admin(self):
        """Register a new admin account"""
        Colors.clear_screen()
        print(f"\n{Colors.PRIMARY}{Colors.BOLD}╔══════════════════════════════════════════════════════════╗{Colors.ENDC}")
        print(f"{Colors.PRIMARY}{Colors.BOLD}║                  REGISTER NEW ADMIN                      ║{Colors.ENDC}")
        print(f"{Colors.PRIMARY}{Colors.BOLD}╚══════════════════════════════════════════════════════════╝{Colors.ENDC}")
        
        # Verify existing admin credentials first
        print(f"\n{Colors.BOLD}Please verify existing admin credentials:{Colors.ENDC}")
        admin_verified = False
        
        attempts = 0
        max_attempts = 3
        
        while attempts < max_attempts:
            existing_username = input(f"\n{Colors.BOLD}Existing Admin Username:{Colors.ENDC} ")
            existing_password = getpass(f"{Colors.BOLD}Existing Admin Password:{Colors.ENDC} ")
            
            print(f"\n{Colors.PRIMARY}Verifying...{Colors.ENDC}")
            self.display_loading_animation(1)
            
            if existing_username in self.admin_credentials and self.admin_credentials[existing_username] == existing_password:
                admin_verified = True
                print(f"\n{Colors.SUCCESS}✓ Admin verified!{Colors.ENDC}")
                break
            else:
                attempts += 1
                remaining = max_attempts - attempts
                if remaining > 0:
                    print(f"\n{Colors.WARNING}! Invalid credentials. {remaining} attempts remaining.{Colors.ENDC}")
                else:
                    print(f"\n{Colors.WARNING}! Maximum verification attempts reached. Registration denied.{Colors.ENDC}")
        
        if not admin_verified:
            input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.ENDC}")
            return
        
        # Get new admin details
        print(f"\n{Colors.BOLD}Enter new admin details:{Colors.ENDC}")
        
        # Username
        while True:
            new_username = input(f"{Colors.BOLD}New Admin Username:{Colors.ENDC} ")
            if not new_username.strip():
                print(f"{Colors.WARNING}! Username cannot be empty.{Colors.ENDC}")
                continue
            
            if new_username in self.admin_credentials:
                print(f"{Colors.WARNING}! Username already exists. Choose another.{Colors.ENDC}")
                continue
            
            break
        
        # Password
        while True:
            new_password = getpass(f"{Colors.BOLD}New Admin Password:{Colors.ENDC} ")
            if not new_password.strip() or len(new_password) < 6:
                print(f"{Colors.WARNING}! Password must be at least 6 characters.{Colors.ENDC}")
                continue
            
            confirm_password = getpass(f"{Colors.BOLD}Confirm Password:{Colors.ENDC} ")
            if new_password != confirm_password:
                print(f"{Colors.WARNING}! Passwords do not match.{Colors.ENDC}")
                continue
            
            break
        
        # Register new admin
        print(f"\n{Colors.PRIMARY}Registering new admin...{Colors.ENDC}")
        self.display_loading_animation(2)
        
        # Add to admin credentials (keeping existing credentials)
        self.admin_credentials[new_username] = new_password
        
        # Save admin credentials
        if self.save_admin_credentials():
            print(f"\n{Colors.SUCCESS}✓ New admin registered successfully!{Colors.ENDC}")
        else:
            print(f"\n{Colors.WARNING}! Error saving admin credentials.{Colors.ENDC}")
        
        input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.ENDC}")

    def admin_login(self):
        """Verify admin credentials"""
        Colors.clear_screen()
        print(f"\n{Colors.PRIMARY}{Colors.BOLD}╔══════════════════════════════════════════════════════════╗{Colors.ENDC}")
        print(f"{Colors.PRIMARY}{Colors.BOLD}║                     ADMIN LOGIN                          ║{Colors.ENDC}")
        print(f"{Colors.PRIMARY}{Colors.BOLD}╚══════════════════════════════════════════════════════════╝{Colors.ENDC}")
        
        attempts = 0
        max_attempts = 3
        
        while attempts < max_attempts:
            username = input(f"\n{Colors.BOLD}Username:{Colors.ENDC} ")
            password = getpass(f"{Colors.BOLD}Password:{Colors.ENDC} ")
            
            print(f"\n{Colors.PRIMARY}Authenticating...{Colors.ENDC}")
            self.display_loading_animation(1)
            
            if username in self.admin_credentials and self.admin_credentials[username] == password:
                print(f"\n{Colors.SUCCESS}✓ Login successful!{Colors.ENDC}")
                return True
            else:
                attempts += 1
                remaining = max_attempts - attempts
                if remaining > 0:
                    print(f"\n{Colors.WARNING}! Invalid credentials. {remaining} attempts remaining.{Colors.ENDC}")
                else:
                    print(f"\n{Colors.WARNING}! Maximum login attempts reached. Access denied.{Colors.ENDC}")
            
        return False

    def admin_flow(self):
        """Handle admin functionality"""
        if not self.admin_login():
            input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.ENDC}")
            return
        
        while True:
            Colors.clear_screen()
            print(f"\n{Colors.PRIMARY}{Colors.BOLD}╔══════════════════════════════════════════════════════════╗{Colors.ENDC}")
            print(f"{Colors.PRIMARY}{Colors.BOLD}║                     ADMIN PANEL                          ║{Colors.ENDC}")
            print(f"{Colors.PRIMARY}{Colors.BOLD}╚══════════════════════════════════════════════════════════╝{Colors.ENDC}")
            
            # Show complaints stats summary
            total = len(self.complaints)
            resolved = len([c for c in self.complaints if c["resolved"]])
            unresolved = total - resolved
            high_priority = len([c for c in self.complaints if c["priority"] == "high"])
            
            print(f"\n{Colors.BOLD}Dashboard Summary:{Colors.ENDC}")
            print(f"  {Colors.PRIMARY}Total Complaints:{Colors.ENDC} {total}")
            print(f"  {Colors.SUCCESS}Resolved:{Colors.ENDC} {resolved}")
            print(f"  {Colors.WARNING}Unresolved:{Colors.ENDC} {unresolved}")
            print(f"  {Colors.WARNING}High Priority:{Colors.ENDC} {high_priority}")
            
            print(f"\n{Colors.BOLD}Select an option:{Colors.ENDC}")
            print(f"  {Colors.PRIMARY}1.{Colors.ENDC} View Recent Complaints (Last 5)")
            print(f"  {Colors.PRIMARY}2.{Colors.ENDC} View All Complaints (Priority Sorted)")
            print(f"  {Colors.PRIMARY}3.{Colors.ENDC} View Resolved Complaints")
            print(f"  {Colors.PRIMARY}4.{Colors.ENDC} View Unresolved Complaints (Priority Sorted)")
            print(f"  {Colors.PRIMARY}5.{Colors.ENDC} Return to Main Menu")
            
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
                print(f"{Colors.WARNING}! Invalid choice. Please try again.{Colors.ENDC}")
                input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.ENDC}")

    def view_complaints(self, filter_type):
        """Display complaints based on filter"""
        Colors.clear_screen()
        filtered_complaints = []
        
        # Make sure priority queue is up to date
        self.update_priority_queue()
        
        # Get all complaints sorted by priority
        sorted_complaints = self.priority_queue.get_all_sorted()
        
        if filter_type == "recent":
            # Get the 5 most recent complaints (time-based, not priority)
            filtered_complaints = sorted(self.complaints, key=lambda x: x["timestamp"], reverse=True)[:5]
            filter_title = "RECENT COMPLAINTS"
        elif filter_type == "all":
            # Use priority-sorted complaints
            filtered_complaints = sorted_complaints
            filter_title = "ALL COMPLAINTS (PRIORITY SORTED)"
        elif filter_type == "resolved":
            filtered_complaints = [c for c in self.complaints if c["resolved"]]
            filter_title = "RESOLVED COMPLAINTS"
        elif filter_type == "unresolved":
            # Filter for unresolved complaints from priority-sorted list
            filtered_complaints = [c for c in sorted_complaints if not c["resolved"]]
            filter_title = "UNRESOLVED COMPLAINTS (PRIORITY SORTED)"
        
        print(f"\n{Colors.PRIMARY}{Colors.BOLD}╔══════════════════════════════════════════════════════════╗{Colors.ENDC}")
        print(f"{Colors.PRIMARY}{Colors.BOLD}║ {filter_title.center(56)} ║{Colors.ENDC}")
        print(f"{Colors.PRIMARY}{Colors.BOLD}╚══════════════════════════════════════════════════════════╝{Colors.ENDC}")
        
        if not filtered_complaints:
            print(f"\n{Colors.PRIMARY}ℹ No complaints found for this category.{Colors.ENDC}")
            input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.ENDC}")
            return
        
        # Display complaints summary
        print(f"\n{Colors.BOLD}{'ID':<5} {'Issue Type':<25} {'Priority':<10} {'Room':<8} {'Status':<12} {'Date':<19}{Colors.ENDC}")
        print(f"{Colors.PRIMARY}{'─' * 80}{Colors.ENDC}")
        
        for c in filtered_complaints:
            status = "Resolved" if c["resolved"] else "Unresolved"
            status_color = Colors.SUCCESS if c["resolved"] else Colors.WARNING
            
            priority_color = Colors.WARNING if c["priority"] == "high" else Colors.SUCCESS
            
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
                    print(f"{Colors.WARNING}! Complaint not found. Please enter a valid ID.{Colors.ENDC}")
            except ValueError:
                print(f"{Colors.WARNING}! Please enter a valid complaint ID.{Colors.ENDC}")
        
        input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.ENDC}")

    def display_complaint_details(self, complaint):
        """Display detailed view of a complaint and allow status update"""
        Colors.clear_screen()
        print(f"\n{Colors.PRIMARY}{Colors.BOLD}╔══════════════════════════════════════════════════════════╗{Colors.ENDC}")
        print(f"{Colors.PRIMARY}{Colors.BOLD}║                 COMPLAINT DETAILS                        ║{Colors.ENDC}")
        print(f"{Colors.PRIMARY}{Colors.BOLD}╚══════════════════════════════════════════════════════════╝{Colors.ENDC}")
        
        status = "Resolved" if complaint['resolved'] else "Unresolved"
        status_color = Colors.SUCCESS if complaint['resolved'] else Colors.WARNING
        
        priority_color = Colors.WARNING if complaint["priority"] == "high" else Colors.SUCCESS
        
        print(f"\n{Colors.PRIMARY}┌──────────────────────────────────────────────────────────┐{Colors.ENDC}")
        print(f"{Colors.PRIMARY}│{Colors.ENDC} {Colors.BOLD}ID:{Colors.ENDC} {complaint['id']:<54} {Colors.PRIMARY}│{Colors.ENDC}")
        print(f"{Colors.PRIMARY}│{Colors.ENDC} {Colors.BOLD}Issue Type:{Colors.ENDC} {complaint['issue_type']:<46} {Colors.PRIMARY}│{Colors.ENDC}")
        print(f"{Colors.PRIMARY}│{Colors.ENDC} {Colors.BOLD}Description:{Colors.ENDC} {complaint['description'][:45]:<44} {Colors.PRIMARY}│{Colors.ENDC}")
    # Handle multi-line descriptions
        description = complaint['description']
        if len(description) > 45:
            print(f"{Colors.PRIMARY}│{Colors.ENDC} {' ' * 13}{description[45:90]:<44} {Colors.PRIMARY}│{Colors.ENDC}")
            if len(description) > 90:
                print(f"{Colors.PRIMARY}│{Colors.ENDC} {' ' * 13}{description[90:135]:<44} {Colors.PRIMARY}│{Colors.ENDC}")
        
        print(f"{Colors.PRIMARY}│{Colors.ENDC} {Colors.BOLD}PC Number:{Colors.ENDC} {complaint['pc_number']:<46} {Colors.PRIMARY}│{Colors.ENDC}")
        print(f"{Colors.PRIMARY}│{Colors.ENDC} {Colors.BOLD}Room Number:{Colors.ENDC} {complaint['room_number']:<44} {Colors.PRIMARY}│{Colors.ENDC}")
        print(f"{Colors.PRIMARY}│{Colors.ENDC} {Colors.BOLD}Student Name:{Colors.ENDC} {complaint['student_name']:<44} {Colors.PRIMARY}│{Colors.ENDC}")
        print(f"{Colors.PRIMARY}│{Colors.ENDC} {Colors.BOLD}Date/Time:{Colors.ENDC} {complaint['timestamp']:<46} {Colors.PRIMARY}│{Colors.ENDC}")
        print(f"{Colors.PRIMARY}│{Colors.ENDC} {Colors.BOLD}Status:{Colors.ENDC} {status_color}{status}{Colors.ENDC}{' ' * (49 - len(status))} {Colors.PRIMARY}│{Colors.ENDC}")
        print(f"{Colors.PRIMARY}│{Colors.ENDC} {Colors.BOLD}Priority:{Colors.ENDC} {priority_color}{complaint['priority'].capitalize()}{Colors.ENDC}{' ' * (47 - len(complaint['priority']))} {Colors.PRIMARY}│{Colors.ENDC}")
        
        # Display additional details if provided
        if complaint['additional_details']:
            print(f"{Colors.PRIMARY}│{Colors.ENDC} {Colors.BOLD}Additional Details:{Colors.ENDC}{' ' * 37} {Colors.PRIMARY}│{Colors.ENDC}")
            details = complaint['additional_details']
            # Handle multi-line additional details with word wrap (max 56 chars per line)
            chunks = [details[i:i+56] for i in range(0, len(details), 56)]
            for chunk in chunks:
                print(f"{Colors.PRIMARY}│{Colors.ENDC} {chunk:<56} {Colors.PRIMARY}│{Colors.ENDC}")
        
        print(f"{Colors.PRIMARY}└──────────────────────────────────────────────────────────┘{Colors.ENDC}")
        
        # Actions menu
        print(f"\n{Colors.BOLD}Available Actions:{Colors.ENDC}")
        print(f"  {Colors.PRIMARY}1.{Colors.ENDC} {'Mark as Resolved' if not complaint['resolved'] else 'Mark as Unresolved'}")
        print(f"  {Colors.PRIMARY}2.{Colors.ENDC} {'Set to Low Priority' if complaint['priority'] == 'high' else 'Set to High Priority'}")
        print(f"  {Colors.PRIMARY}3.{Colors.ENDC} Return to Complaints List")
        
        action = input(f"\n{Colors.BOLD}Select action (1-3):{Colors.ENDC} ")
        
        if action == "1":
            # Toggle resolved status
            complaint['resolved'] = not complaint['resolved']
            new_status = "Resolved" if complaint['resolved'] else "Unresolved"
            
            print(f"\n{Colors.PRIMARY}Updating complaint status...{Colors.ENDC}")
            self.display_loading_animation(1)
            
            if self.save_complaints():
                print(f"\n{Colors.SUCCESS}✓ Complaint status updated to {new_status}!{Colors.ENDC}")
            else:
                print(f"\n{Colors.WARNING}! Failed to update complaint status.{Colors.ENDC}")
        
        elif action == "2":
            # Toggle priority
            new_priority = "low" if complaint['priority'] == "high" else "high"
            complaint['priority'] = new_priority
            
            print(f"\n{Colors.PRIMARY}Updating complaint priority...{Colors.ENDC}")
            self.display_loading_animation(1)
            
            if self.save_complaints():
                print(f"\n{Colors.SUCCESS}✓ Complaint priority updated to {new_priority.capitalize()}!{Colors.ENDC}")
            else:
                print(f"\n{Colors.WARNING}! Failed to update complaint priority.{Colors.ENDC}")

    def run(self):
        """Main application loop"""
        while True:
            self.display_welcome()
            role = self.get_role()
            
            if role == "student":
                self.student_flow()
            elif role == "admin":
                self.admin_flow()
            elif role == "register":
                self.register_admin()
            elif role == "exit":
                Colors.clear_screen()
                
                # Enhanced exit message
                exit_message = f"""\
{Colors.SECONDARY}{Colors.BOLD}🎉 LabAssist Exit: A Journey of Innovation 🚀{Colors.ENDC}

{Colors.SUCCESS}You've successfully exited LabAssist – but the mission to make lab life easier never stops!{Colors.ENDC}
{Colors.PRIMARY}Thanks for being part of the solution. Whether you're reporting an issue or resolving one,
you've just helped create a smoother, smarter lab experience. 💻⚙️🔒 Your efforts may seem small, but they're part of something bigger – a culture of care, efficiency, and 
accountability inside the lab.{Colors.ENDC}

{Colors.BOLD}🏆 Our Amazing Team{Colors.ENDC}
{Colors.PRIMARY}
            🚀 Charles Christopher B. Organista – Lead Developer
            📚 Kate Mergelaine A. Lacanlali – Documentation Specialist
            🧩 Phillip Kaizer L. Lagrana – Algorithm Designer
            🔧 John Arnold B. Oloteo – Tester / Debugger{Colors.ENDC}

            {Colors.BOLD}🏫 Our Home{Colors.ENDC}
            {Colors.PRIMARY}Proudly crafted at:
            LORMA Colleges – College of Computer Studies and Engineering
            📅 Academic Year 2024–2025{Colors.ENDC}

            {Colors.BOLD}💬 Our Motto{Colors.ENDC}
            {Colors.SUCCESS}"We don't just code to pass, we code to make an impact."{Colors.ENDC}

            {Colors.PRIMARY}✨ Innovation begins when we care enough to solve real problems.
            🚪 Exiting now... but our code continues to care.

            🎯 Stay sharp. Stay helpful. Stay TECHTITANIC. 💙💡
            ✨ Until the next session... keep making a difference.
            ✨ See you next log-in! Until then... stay smart, stay helpful, and stay TECHTITANIC! 💙{Colors.ENDC}
            """
                
                # Print the exit message with color formatting
                print(exit_message)
                break


if __name__ == "__main__":
    # Instantiate and run the application
    app = LabAssist()
    app.run()
