"""
seed.py - Dummy Data Seeder for Servisio

Purpose:
    Populates the database with sample users, incidents,
    service requests, and knowledge base articles.

Usage:
    Run once after creating the database:
        python seed.py
"""

from app import create_app
from models import db, User, Incident, ServiceRequest, KBArticle
from datetime import datetime, timedelta
import random

app = create_app()
app.app_context().push()

# Drop and recreate tables (optional for fresh start)
db.drop_all()
db.create_all()

# --- Users ---
random.seed(42)

first_names = [
    "Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Jamie", "Sam",
    "Avery", "Quinn", "Drew", "Kai"
]
roles = ["Admin", "Technician", "User", "User", "User"]

users = []
for idx, name in enumerate(first_names, start=1):
    role = roles[0] if idx == 1 else (roles[1] if idx in (2, 3) else random.choice(roles[2:]))
    username = name.lower() + str(idx)
    email = f"{username}@servisio.com"
    password = ("admin123" if role == "Admin" else ("tech123" if role == "Technician" else "user123"))
    users.append(User(username=username, email=email, password=password, role=role))

db.session.add_all(users)
db.session.commit()

user_ids = [u.id for u in users]
technician_ids = [u.id for u in users if u.role == "Technician"]


# --- Incidents ---
incidents_data = [
    {
        "title": "Critical: Exchange Server Outage - Email Services Down",
        "description": "Complete email service failure affecting all 500+ users. Exchange server showing 'Service Unavailable' errors. Users cannot send or receive emails. Outlook clients showing 'Cannot connect to server' messages. Emergency escalation required as this impacts business operations across all departments.",
        "category": "Network"
    },
    {
        "title": "High Priority: Network Switch Failure in Building A",
        "description": "Core network switch in Building A has failed, causing complete network outage for 150+ users on floors 2-4. Users reporting 'No internet connection' and 'Network cable unplugged' errors. VoIP phones also down. Estimated business impact: $50,000/hour in lost productivity.",
        "category": "Network"
    },
    {
        "title": "Software: Adobe Creative Suite License Expired",
        "description": "Adobe Creative Suite licenses expired overnight, affecting 25+ designers and marketing team members. Users getting 'License expired' popup messages and cannot access Photoshop, Illustrator, or InDesign. Workflow completely halted for creative projects. Need immediate license renewal or temporary workaround.",
        "category": "Software"
    },
    {
        "title": "Hardware: Multiple Laptop Battery Failures",
        "description": "15+ Dell Latitude 5520 laptops experiencing rapid battery drain and 'Battery critically low' warnings within 2 hours of unplugged use. Batteries not holding charge, some laptops shutting down unexpectedly. Affecting mobile workforce and remote employees. Potential hardware defect or firmware issue.",
        "category": "Hardware"
    },
    {
        "title": "Critical: Database Server Performance Degradation",
        "description": "Primary SQL Server experiencing severe performance issues with 15-second query response times. ERP system timing out, users unable to process orders or access customer data. Database showing 95% CPU utilization and memory pressure. Business-critical system affecting revenue operations.",
        "category": "Software"
    },
    {
        "title": "Network: VPN Connection Drops Every 30 Minutes",
        "description": "Remote users experiencing frequent VPN disconnections with 'Connection lost' errors every 30-45 minutes. Users must reconnect multiple times per day, causing workflow interruptions. Affecting 200+ remote workers. VPN logs show authentication timeouts and tunnel failures.",
        "category": "Network"
    },
    {
        "title": "Hardware: Printer Paper Jam in High-Volume Copier",
        "description": "Xerox WorkCentre 7845 showing persistent 'Paper jam in tray 2' error despite multiple clearing attempts. Paper path sensors may be faulty. Affecting document printing for entire finance department (50+ users). Manual workarounds causing 2-hour delays in report generation.",
        "category": "Hardware"
    },
    {
        "title": "Software: Windows 11 Update Breaking Legacy Applications",
        "description": "Recent Windows 11 cumulative update (KB5034441) causing compatibility issues with legacy accounting software. Application crashes with 'Access violation' errors. 12 users affected in accounting department. Rollback not possible due to security requirements. Need compatibility fix or software update.",
        "category": "Software"
    },
    {
        "title": "Network: DNS Resolution Failures Across Campus",
        "description": "Intermittent DNS resolution failures affecting internal and external website access. Users getting 'DNS_PROBE_FINISHED_NXDOMAIN' errors. Some websites load while others don't. Primary DNS server showing high response times. Affecting 300+ users across multiple buildings.",
        "category": "Network"
    },
    {
        "title": "Hardware: Server Room UPS Battery Backup Failure",
        "description": "Main UPS system in server room showing 'Battery failure' alarm. Battery backup time reduced from 30 minutes to 2 minutes. Risk of data loss during power outages. Critical infrastructure issue requiring immediate battery replacement. Server room contains 15 production servers.",
        "category": "Hardware"
    },
    {
        "title": "Software: Microsoft Teams Audio/Video Issues",
        "description": "Teams meetings experiencing audio echo, video freezing, and 'Poor network quality' warnings. Users reporting dropped calls and poor audio quality. Affecting 100+ daily meeting participants. Network bandwidth tests show adequate speeds. Potential Teams service or client configuration issue.",
        "category": "Software"
    },
    {
        "title": "Hardware: Multiple Monitor Display Issues",
        "description": "Dual monitor setups showing 'No signal' on secondary displays after Windows updates. 40+ users affected with productivity loss. Display drivers may be corrupted. Some users can't extend desktop, others getting 'Display driver stopped responding' errors. Need driver rollback or reinstallation.",
        "category": "Hardware"
    },
    {
        "title": "Network: Firewall Blocking Legitimate Business Applications",
        "description": "Corporate firewall recently updated and now blocking access to Salesforce, Dropbox, and other business-critical cloud applications. Users getting 'Connection blocked by firewall' errors. Security team needs to whitelist domains while maintaining security posture. Affecting 200+ users.",
        "category": "Network"
    },
    {
        "title": "Software: Antivirus False Positives Quarantining Business Files",
        "description": "Symantec Endpoint Protection flagging legitimate business documents as malware and quarantining them. 50+ files quarantined including Excel reports, PDF contracts, and Word documents. Users cannot access critical business files. Need to restore files and update antivirus definitions.",
        "category": "Software"
    },
    {
        "title": "Hardware: Server Hard Drive Showing SMART Errors",
        "description": "Production file server showing SMART errors on primary hard drive. Drive health at 15% with increasing bad sectors. Risk of complete drive failure and data loss. 2TB of shared files at risk. Need immediate drive replacement and data migration. Users may experience slow file access.",
        "category": "Hardware"
    },
    {
        "title": "Network: Wireless Access Point Overload in Conference Rooms",
        "description": "Conference rooms experiencing poor Wi-Fi connectivity during meetings. Access points showing 95% utilization with 50+ concurrent connections. Users getting 'Weak signal' and frequent disconnections. Need additional access points or bandwidth optimization for high-density areas.",
        "category": "Network"
    },
    {
        "title": "Software: SharePoint Document Library Sync Failures",
        "description": "SharePoint Online document libraries not syncing properly with OneDrive client. Users seeing 'Sync error' messages and missing recent document updates. 75+ users affected with document version conflicts. Need to reset sync and reconfigure OneDrive client settings.",
        "category": "Software"
    },
    {
        "title": "Hardware: Keyboard and Mouse Not Responding After Sleep",
        "description": "Dell OptiPlex workstations not responding to keyboard/mouse input after system sleep mode. Users must hard reboot to restore functionality. Affecting 30+ workstations. USB power management or driver issue suspected. Productivity impact as users lose work in progress.",
        "category": "Hardware"
    },
    {
        "title": "Network: Internet Bandwidth Saturation During Peak Hours",
        "description": "Corporate internet connection experiencing severe slowdowns during 9-11 AM and 2-4 PM. Users reporting 'Slow internet' and timeouts on cloud applications. Bandwidth utilization at 95% during peak hours. Need bandwidth upgrade or traffic shaping policies to prioritize business applications.",
        "category": "Network"
    },
    {
        "title": "Software: Active Directory Authentication Delays",
        "description": "Users experiencing 30-60 second delays when logging into Windows workstations. Active Directory authentication taking unusually long, causing login timeouts for some users. Domain controllers showing high CPU usage. Affecting 400+ users across the organization. Need AD performance optimization.",
        "category": "Software"
    }
]

incident_statuses = ["Open", "In Progress", "Resolved", "Closed"]
priorities = ["Low", "Medium", "High"]

now = datetime.utcnow()
incidents = []
for i in range(20):  # Use exactly 20 incidents as requested
    incident_data = incidents_data[i]
    created_by = random.choice(user_ids)
    priority = random.choices(priorities, weights=[0.3, 0.5, 0.2])[0]
    status = random.choices(incident_statuses, weights=[0.35, 0.35, 0.2, 0.1])[0]
    created_offset_days = random.randint(0, 45)
    created_at = now - timedelta(days=created_offset_days, hours=random.randint(0, 23), minutes=random.randint(0, 59))
    # If resolved/closed, set updated_at after created_at by 1–72 hours; else set recent update
    if status in ("Resolved", "Closed"):
        hours_to_resolve = random.randint(1, 72)
        updated_at = created_at + timedelta(hours=hours_to_resolve, minutes=random.randint(0, 59))
    else:
        updated_at = created_at + timedelta(hours=random.randint(0, 24), minutes=random.randint(0, 59))

    incidents.append(Incident(
        title=incident_data["title"],
        description=incident_data["description"],
        status=status,
        priority=priority,
        created_by=created_by,
        created_at=created_at,
        updated_at=updated_at
    ))

db.session.add_all(incidents)
db.session.commit()

# --- Service Requests ---
sr_titles = [
    "Request new mouse",
    "Request software installation",
    "New laptop request",
    "Extra monitor setup",
    "Access to finance folder",
    "Create email distribution list",
    "VPN access request",
    "Install Adobe Acrobat",
    "Upgrade to Windows 11",
    "Request for admin rights",
    "New account creation",
    "Password reset",
    "Provision virtual machine",
    "Request new headset",
    "Install Python environment",
    "Install Node.js",
    "Shared mailbox access",
    "Jira project access",
    "Slack channel creation",
    "Request docking station"
]
sr_statuses = ["Pending", "Approved", "Completed", "Rejected"]
sr_types = ["Hardware", "Software", "Network", "Access", "Accounts"]

services = []
for i in range(30):
    title = random.choice(sr_titles)
    created_by = random.choice(user_ids)
    request_type = random.choices(sr_types, weights=[0.35, 0.35, 0.15, 0.1, 0.05])[0]
    status = random.choices(sr_statuses, weights=[0.4, 0.25, 0.3, 0.05])[0]
    created_offset_days = random.randint(0, 45)
    created_at = now - timedelta(days=created_offset_days, hours=random.randint(0, 23), minutes=random.randint(0, 59))
    updated_at = created_at + timedelta(hours=random.randint(1, 48))
    services.append(ServiceRequest(
        title=title,
        description=f"{title} submitted by user for fulfillment.",
        status=status,
        request_type=request_type,
        created_by=created_by,
        created_at=created_at,
        updated_at=updated_at
    ))

db.session.add_all(services)
db.session.commit()

# --- Knowledge Base Articles ---
kb_items = [
    (
        "Exchange Server Outage Recovery Procedures",
        """# Exchange Server Outage Recovery Guide

## Immediate Response Steps
1. **Verify Service Status**: Check Exchange Admin Center for service health indicators
2. **Check Event Logs**: Review Application and System logs for critical errors
3. **Verify Database Status**: Ensure Exchange databases are mounted and healthy
4. **Check DAG Status**: If using Database Availability Groups, verify replication status

## Common Resolution Steps
1. **Restart Exchange Services**:
   - Open Services.msc as Administrator
   - Restart Microsoft Exchange Information Store
   - Restart Microsoft Exchange System Attendant
   - Restart Microsoft Exchange Transport

2. **Database Recovery**:
   - Use Eseutil to check database integrity
   - Run: `eseutil /mh "C:\Program Files\Microsoft\Exchange Server\V15\Mailbox\database.edb"`
   - If corrupted, restore from backup or repair using eseutil /p

3. **IIS Reset**:
   - Open IIS Manager
   - Right-click on server name → All Tasks → Restart
   - Or run: `iisreset /restart`

## Prevention Measures
- Implement proper backup procedures
- Monitor disk space and performance
- Keep Exchange updated with latest patches
- Configure proper DAG replication

## Escalation
If issues persist after 30 minutes, escalate to Exchange administrator or Microsoft support.""",
        "Network"
    ),
    (
        "Network Switch Failure Troubleshooting",
        """# Network Switch Failure Recovery Guide

## Initial Assessment
1. **Physical Inspection**:
   - Check power LED status
   - Verify all cable connections
   - Look for any physical damage or overheating
   - Check for loose or damaged ports

2. **Power Cycle Procedure**:
   - Disconnect power cable for 30 seconds
   - Reconnect and wait for full boot sequence
   - Monitor LED patterns during startup

## Advanced Troubleshooting
1. **Console Access**:
   - Connect via console cable to management port
   - Check boot sequence and error messages
   - Verify configuration integrity

2. **Port Status Check**:
   - Use `show interface status` command
   - Identify failed or error-disabled ports
   - Check for port security violations

3. **VLAN Configuration**:
   - Verify VLAN assignments with `show vlan brief`
   - Check trunk port configurations
   - Ensure proper VLAN routing

## Recovery Steps
1. **Factory Reset** (if needed):
   - Hold reset button for 10 seconds during boot
   - Restore configuration from backup
   - Reconfigure VLANs and port settings

2. **Firmware Update**:
   - Download latest firmware from vendor
   - Use TFTP or console to update
   - Verify update completion

## Prevention
- Regular firmware updates
- Environmental monitoring (temperature, humidity)
- Redundant power supplies
- Proper cable management""",
        "Network"
    ),
    (
        "Adobe Creative Suite License Management",
        """# Adobe Creative Suite License Resolution

## License Issue Diagnosis
1. **Check License Status**:
   - Open Creative Cloud Desktop app
   - Go to Account → Manage Plan
   - Verify subscription status and expiration date

2. **Common Error Messages**:
   - "License expired" - Subscription needs renewal
   - "Too many activations" - Deactivate unused devices
   - "Server unavailable" - Network or Adobe server issue

## Resolution Steps
1. **License Renewal**:
   - Contact IT procurement for license renewal
   - Update payment information if needed
   - Wait 24-48 hours for license propagation

2. **Device Management**:
   - Deactivate unused devices in Adobe account
   - Maximum 2 activations per license
   - Use Adobe website to manage devices

3. **Offline Activation**:
   - Download offline installer from Adobe
   - Use serial number for activation
   - Contact Adobe support for offline codes

## Temporary Workarounds
1. **Trial Mode**:
   - Use 7-day trial while waiting for license
   - Save work frequently as trials have limitations
   - Export projects in compatible formats

2. **Alternative Software**:
   - GIMP for image editing
   - Inkscape for vector graphics
   - Scribus for desktop publishing

## Prevention
- Set up license expiration alerts
- Maintain device activation records
- Regular license audits
- Backup license information""",
        "Software"
    ),
    (
        "Laptop Battery Failure Diagnosis and Resolution",
        """# Laptop Battery Failure Troubleshooting

## Initial Diagnosis
1. **Battery Health Check**:
   - Run Windows battery report: `powercfg /batteryreport`
   - Check battery capacity vs. design capacity
   - Look for "Replace Soon" or "Replace Now" warnings

2. **Physical Inspection**:
   - Check for battery swelling or damage
   - Verify battery connection to motherboard
   - Look for corrosion on battery contacts

## Software Solutions
1. **Battery Calibration**:
   - Charge to 100%, then drain completely
   - Repeat cycle 2-3 times
   - Use manufacturer's calibration tool if available

2. **Power Management Reset**:
   - Uninstall battery drivers in Device Manager
   - Restart computer to reinstall drivers
   - Reset power plan to balanced

3. **BIOS Update**:
   - Check manufacturer website for BIOS updates
   - Update BIOS to latest version
   - Reset BIOS to default settings

## Hardware Solutions
1. **Battery Replacement**:
   - Order genuine replacement battery
   - Follow manufacturer's replacement guide
   - Dispose of old battery properly

2. **Power Adapter Check**:
   - Test with different power adapter
   - Verify adapter wattage matches requirements
   - Check for damaged charging port

## Prevention Measures
- Avoid extreme temperatures
- Don't leave laptop plugged in constantly
- Use battery saver mode when possible
- Regular battery health monitoring""",
        "Hardware"
    ),
    (
        "SQL Server Performance Optimization",
        """# SQL Server Performance Degradation Resolution

## Performance Analysis
1. **Identify Bottlenecks**:
   - Use SQL Server Management Studio Activity Monitor
   - Check CPU, Memory, and I/O utilization
   - Review wait statistics and blocking sessions

2. **Query Analysis**:
   - Use SQL Profiler to identify slow queries
   - Check execution plans for missing indexes
   - Review query statistics and cache hit ratios

## Immediate Resolution Steps
1. **Kill Blocking Sessions**:
   ```sql
   SELECT session_id, blocking_session_id, wait_type, wait_time
   FROM sys.dm_exec_requests
   WHERE blocking_session_id > 0
   ```

2. **Clear Plan Cache** (if needed):
   ```sql
   DBCC FREEPROCCACHE
   ```

3. **Restart SQL Services**:
   - Stop SQL Server service
   - Wait 30 seconds
   - Start SQL Server service

## Long-term Optimization
1. **Index Maintenance**:
   - Rebuild fragmented indexes
   - Update statistics regularly
   - Add missing indexes based on query analysis

2. **Memory Configuration**:
   - Set max server memory appropriately
   - Enable Lock Pages in Memory
   - Configure tempdb on separate drives

3. **Storage Optimization**:
   - Separate data, log, and tempdb files
   - Use SSD storage for critical databases
   - Implement proper backup strategy

## Monitoring Setup
- Configure SQL Server alerts
- Set up performance monitoring
- Regular maintenance plan execution
- Database growth monitoring""",
        "Software"
    ),
    (
        "VPN Connection Stability Issues",
        """# VPN Connection Drop Troubleshooting

## Connection Analysis
1. **Log Analysis**:
   - Check VPN client logs for error messages
   - Review server-side authentication logs
   - Look for timeout patterns and error codes

2. **Network Testing**:
   - Test internet connectivity without VPN
   - Check DNS resolution times
   - Verify firewall and proxy settings

## Client-Side Solutions
1. **VPN Client Configuration**:
   - Update VPN client to latest version
   - Clear saved credentials and reconnect
   - Adjust connection timeout settings

2. **Network Adapter Reset**:
   - Disable and re-enable network adapters
   - Reset TCP/IP stack: `netsh int ip reset`
   - Clear DNS cache: `ipconfig /flushdns`

3. **Power Management**:
   - Disable network adapter power saving
   - Prevent Windows from turning off network adapters
   - Check USB power management for USB adapters

## Server-Side Solutions
1. **Session Timeout Adjustment**:
   - Increase idle timeout settings
   - Configure keep-alive intervals
   - Adjust authentication timeout values

2. **Load Balancing**:
   - Distribute VPN connections across servers
   - Implement session affinity
   - Monitor server resource utilization

## Advanced Troubleshooting
1. **MTU Size Adjustment**:
   - Test with different MTU sizes
   - Use ping with DF flag to find optimal size
   - Configure client MTU settings

2. **Protocol Optimization**:
   - Try different VPN protocols (OpenVPN, IPSec, SSTP)
   - Adjust encryption levels
   - Configure compression settings

## Prevention
- Regular VPN server maintenance
- Monitor connection patterns
- Implement redundant VPN servers
- User training on connection best practices""",
        "Network"
    ),
    (
        "High-Volume Printer Paper Jam Resolution",
        """# Xerox WorkCentre Paper Jam Troubleshooting

## Safety First
- Turn off printer and unplug power cord
- Allow printer to cool for 10 minutes
- Wear gloves to protect from sharp edges

## Paper Jam Location Identification
1. **Check Display Messages**:
   - Note specific error code and tray location
   - Look for paper path indicators on display
   - Check for multiple jam locations

2. **Visual Inspection**:
   - Open all access doors and trays
   - Look for torn paper pieces
   - Check for foreign objects in paper path

## Systematic Jam Removal
1. **Tray 2 Specific Steps**:
   - Remove paper from tray 2 completely
   - Check for paper stuck in feed rollers
   - Inspect separation pad for wear
   - Clean feed rollers with lint-free cloth

2. **Paper Path Cleaning**:
   - Remove all visible paper pieces
   - Use compressed air to clear debris
   - Check for damaged sensors
   - Clean all rollers and guides

3. **Sensor Reset**:
   - Close all doors and trays
   - Power on printer
   - Wait for initialization to complete
   - Test with small paper load

## Preventive Maintenance
1. **Paper Quality**:
   - Use recommended paper types
   - Avoid damp or curled paper
   - Don't mix different paper types
   - Store paper in proper conditions

2. **Regular Cleaning**:
   - Clean feed rollers monthly
   - Replace worn separation pads
   - Check and clean sensors
   - Lubricate moving parts as needed

## Advanced Solutions
1. **Sensor Replacement**:
   - If sensors are faulty, replace them
   - Calibrate new sensors properly
   - Update firmware if needed

2. **Professional Service**:
   - Contact Xerox service for complex issues
   - Schedule regular maintenance
   - Keep service contract current""",
        "Hardware"
    ),
    (
        "Windows 11 Legacy Application Compatibility",
        """# Windows 11 Legacy App Compatibility Issues

## Compatibility Assessment
1. **Application Analysis**:
   - Check application compatibility with Windows 11
   - Review vendor support status
   - Identify specific compatibility issues

2. **Error Analysis**:
   - Review Windows Event Viewer logs
   - Check application crash dumps
   - Look for specific error codes

## Immediate Solutions
1. **Compatibility Mode**:
   - Right-click application executable
   - Properties → Compatibility tab
   - Run in Windows 10 compatibility mode
   - Enable "Run as administrator"

2. **Registry Modifications**:
   - Create compatibility shims
   - Modify application registry entries
   - Use Application Compatibility Toolkit (ACT)

3. **Virtual Machine Solution**:
   - Install Windows 10 VM for legacy apps
   - Use Hyper-V or VMware
   - Configure seamless integration

## Advanced Solutions
1. **Application Virtualization**:
   - Use Microsoft App-V
   - Package application in virtual environment
   - Deploy through enterprise systems

2. **Dual Boot Setup**:
   - Install Windows 10 alongside Windows 11
   - Boot to Windows 10 for legacy apps
   - Share data between systems

## Long-term Solutions
1. **Application Updates**:
   - Contact vendor for Windows 11 support
   - Upgrade to newer application versions
   - Consider alternative applications

2. **System Rollback**:
   - Use Windows 11 rollback feature
   - Restore to previous Windows version
   - Plan migration timeline

## Prevention
- Test applications before Windows 11 upgrade
- Maintain compatibility database
- Plan application modernization
- Keep legacy systems for critical apps""",
        "Software"
    ),
    (
        "DNS Resolution Failure Troubleshooting",
        """# DNS Resolution Issues Resolution Guide

## Initial Diagnosis
1. **DNS Testing**:
   - Test with: `nslookup google.com`
   - Check: `ping 8.8.8.8` (Google DNS)
   - Verify: `ipconfig /all` for DNS settings

2. **Common Error Messages**:
   - DNS_PROBE_FINISHED_NXDOMAIN
   - DNS_PROBE_FINISHED_NO_INTERNET
   - DNS server not responding

## Client-Side Solutions
1. **DNS Cache Clear**:
   - Run: `ipconfig /flushdns`
   - Restart DNS client service
   - Clear browser DNS cache

2. **DNS Server Change**:
   - Use public DNS: 8.8.8.8, 8.8.4.4
   - Configure in network adapter settings
   - Test with different DNS providers

3. **Network Adapter Reset**:
   - Disable and re-enable network adapter
   - Reset TCP/IP stack
   - Restart network services

## Server-Side Solutions
1. **DNS Server Health Check**:
   - Verify DNS service is running
   - Check server resource utilization
   - Review DNS server logs

2. **DNS Configuration**:
   - Verify forwarders are configured
   - Check root hints configuration
   - Validate zone file integrity

3. **DNS Server Restart**:
   - Stop DNS service gracefully
   - Clear DNS server cache
   - Restart DNS service

## Advanced Troubleshooting
1. **DNS Monitoring**:
   - Use DNS monitoring tools
   - Set up DNS health alerts
   - Monitor query response times

2. **Load Balancing**:
   - Configure multiple DNS servers
   - Implement DNS round-robin
   - Use DNS failover mechanisms

## Prevention
- Regular DNS server maintenance
- Monitor DNS performance
- Keep DNS servers updated
- Implement DNS redundancy""",
        "Network"
    ),
    (
        "UPS Battery Backup System Maintenance",
        """# UPS Battery Backup Failure Resolution

## Safety Precautions
- Turn off UPS and disconnect from power
- Allow system to cool completely
- Use proper personal protective equipment
- Follow manufacturer safety guidelines

## Battery Health Assessment
1. **Visual Inspection**:
   - Check for battery swelling or leakage
   - Look for corrosion on terminals
   - Verify battery connections are secure

2. **Battery Testing**:
   - Use UPS self-test function
   - Check battery voltage with multimeter
   - Monitor battery runtime during test

## Battery Replacement Procedure
1. **Preparation**:
   - Document current UPS configuration
   - Ensure proper replacement batteries
   - Have backup power source ready

2. **Replacement Steps**:
   - Remove old batteries carefully
   - Clean battery compartment
   - Install new batteries with correct polarity
   - Secure all connections

3. **Testing**:
   - Power on UPS system
   - Run self-test procedure
   - Verify proper battery charging
   - Test runtime under load

## Maintenance Schedule
1. **Regular Tasks**:
   - Monthly visual inspection
   - Quarterly battery testing
   - Annual professional service
   - Keep maintenance logs

2. **Environmental Monitoring**:
   - Maintain proper temperature (20-25°C)
   - Control humidity levels
   - Ensure adequate ventilation
   - Monitor for dust accumulation

## Advanced Solutions
1. **Battery Monitoring**:
   - Install battery monitoring software
   - Set up automated alerts
   - Track battery health trends
   - Plan replacement schedules

2. **Redundancy**:
   - Install redundant UPS systems
   - Configure automatic failover
   - Implement load sharing
   - Regular failover testing

## Prevention
- Follow manufacturer maintenance schedule
- Monitor battery age and cycles
- Maintain proper environmental conditions
- Keep spare batteries on hand""",
        "Hardware"
    ),
    (
        "Microsoft Teams Audio/Video Troubleshooting",
        """# Microsoft Teams Audio/Video Issues Resolution

## Audio Issues Diagnosis
1. **Device Testing**:
   - Test microphone in Windows Sound settings
   - Check speaker/headphone functionality
   - Verify device permissions in Teams

2. **Audio Settings**:
   - Go to Teams Settings → Devices
   - Test microphone and speakers
   - Adjust volume levels appropriately

## Video Issues Diagnosis
1. **Camera Testing**:
   - Test camera in Windows Camera app
   - Check camera permissions
   - Verify camera is not used by other apps

2. **Video Settings**:
   - Go to Teams Settings → Devices
   - Test camera functionality
   - Adjust video quality settings

## Network Optimization
1. **Bandwidth Testing**:
   - Run speed test (speedtest.net)
   - Check for network congestion
   - Verify adequate upload/download speeds

2. **Network Configuration**:
   - Use wired connection when possible
   - Close unnecessary applications
   - Configure QoS for Teams traffic

## Advanced Solutions
1. **Teams Client Reset**:
   - Clear Teams cache and data
   - Reset Teams to default settings
   - Reinstall Teams client if needed

2. **System Optimization**:
   - Update audio/video drivers
   - Disable hardware acceleration
   - Adjust Windows power settings

## Server-Side Solutions
1. **Teams Admin Center**:
   - Check service health status
   - Review meeting policies
   - Verify network configuration

2. **Network Configuration**:
   - Configure proper firewall rules
   - Set up Teams traffic prioritization
   - Implement bandwidth management

## Prevention
- Regular driver updates
- Network monitoring and optimization
- User training on Teams features
- Regular system maintenance""",
        "Software"
    ),
    (
        "Multiple Monitor Display Issues Resolution",
        """# Dual Monitor Display Problems Troubleshooting

## Initial Diagnosis
1. **Connection Check**:
   - Verify all cable connections
   - Test with different cables
   - Check for damaged ports

2. **Display Detection**:
   - Press Windows + P to check display modes
   - Go to Display Settings
   - Click "Detect" to find monitors

## Driver Solutions
1. **Driver Update**:
   - Update graphics card drivers
   - Use manufacturer's latest drivers
   - Restart after driver installation

2. **Driver Rollback**:
   - Device Manager → Display adapters
   - Right-click graphics card → Properties
   - Rollback driver if recent update caused issues

## Display Configuration
1. **Display Settings**:
   - Right-click desktop → Display settings
   - Arrange displays correctly
   - Set appropriate resolution for each monitor

2. **Advanced Display Settings**:
   - Click "Advanced display settings"
   - Set refresh rate appropriately
   - Configure color depth and profile

## Hardware Solutions
1. **Port Testing**:
   - Try different video ports (HDMI, DisplayPort, VGA)
   - Test with different monitors
   - Check for port damage

2. **Graphics Card**:
   - Reseat graphics card if possible
   - Check for overheating issues
   - Test with integrated graphics

## Advanced Troubleshooting
1. **Registry Fixes**:
   - Reset display registry entries
   - Clear display cache
   - Rebuild display database

2. **System File Check**:
   - Run: `sfc /scannow`
   - Check for corrupted system files
   - Repair if issues found

## Prevention
- Regular driver updates
- Proper cable management
- Monitor power management settings
- Regular system maintenance""",
        "Hardware"
    ),
    (
        "Firewall Application Blocking Resolution",
        """# Firewall Blocking Business Applications

## Application Analysis
1. **Identify Blocked Applications**:
   - Check firewall logs for blocked connections
   - Review application error messages
   - Test application connectivity

2. **Port and Protocol Requirements**:
   - Identify required ports and protocols
   - Check application documentation
   - Verify network requirements

## Firewall Configuration
1. **Application Whitelisting**:
   - Add applications to firewall exceptions
   - Configure both inbound and outbound rules
   - Test application functionality

2. **Port Rules**:
   - Create specific port rules for applications
   - Configure protocol-specific rules
   - Set appropriate scope and profiles

## Network-Level Solutions
1. **Proxy Configuration**:
   - Configure proxy settings for applications
   - Add proxy exceptions for business apps
   - Test proxy connectivity

2. **VPN Configuration**:
   - Configure split tunneling if needed
   - Route business apps through VPN
   - Test VPN application routing

## Advanced Solutions
1. **Deep Packet Inspection**:
   - Configure DPI rules for applications
   - Allow specific application signatures
   - Monitor for false positives

2. **Application Control**:
   - Implement application control policies
   - Create application-specific rules
   - Monitor application usage

## Security Considerations
1. **Risk Assessment**:
   - Evaluate security implications
   - Implement least privilege access
   - Monitor for security threats

2. **Compliance**:
   - Ensure compliance with security policies
   - Document firewall rule changes
   - Regular security audits

## Prevention
- Regular firewall rule reviews
- Application requirement documentation
- Security policy updates
- Regular security training""",
        "Network"
    ),
    (
        "Antivirus False Positive Resolution",
        """# Antivirus False Positive File Recovery

## Immediate Response
1. **Quarantine Assessment**:
   - Check antivirus quarantine folder
   - Identify quarantined business files
   - Document file types and locations

2. **Business Impact**:
   - Assess affected users and departments
   - Identify critical business files
   - Prioritize recovery efforts

## File Recovery Process
1. **Restore from Quarantine**:
   - Open antivirus management console
   - Navigate to quarantine section
   - Restore legitimate business files
   - Add files to exclusion list

2. **Exclusion Configuration**:
   - Add file extensions to exclusions
   - Exclude specific folders if needed
   - Configure real-time scanning exclusions

## Antivirus Configuration
1. **Definition Updates**:
   - Update antivirus definitions
   - Check for known false positive fixes
   - Restart antivirus service

2. **Scanning Policies**:
   - Adjust scanning sensitivity
   - Configure file type exclusions
   - Set up custom scan policies

## Advanced Solutions
1. **Sandbox Analysis**:
   - Submit files for sandbox analysis
   - Contact antivirus vendor support
   - Request false positive review

2. **Alternative Scanning**:
   - Use multiple antivirus engines
   - Implement cloud-based scanning
   - Configure behavioral analysis

## Prevention Measures
1. **File Management**:
   - Implement proper file naming conventions
   - Use digital signatures for business files
   - Regular file integrity checks

2. **Antivirus Management**:
   - Regular definition updates
   - Monitor for false positive reports
   - Maintain exclusion lists

## Documentation
- Document all recovered files
- Maintain exclusion list documentation
- Regular antivirus policy reviews
- User training on file handling""",
        "Software"
    ),
    (
        "Server Hard Drive SMART Error Resolution",
        """# Server Hard Drive SMART Error Recovery

## Critical Assessment
1. **SMART Data Analysis**:
   - Check SMART attributes using manufacturer tools
   - Identify specific failing attributes
   - Assess drive health percentage

2. **Data Backup Priority**:
   - Immediately backup critical data
   - Verify backup integrity
   - Document data locations and sizes

## Immediate Actions
1. **Data Migration**:
   - Copy data to healthy drives
   - Verify data integrity after copy
   - Update file system permissions

2. **Drive Replacement**:
   - Order replacement drive immediately
   - Plan for minimal downtime
   - Prepare migration procedures

## Replacement Procedure
1. **Pre-Replacement**:
   - Complete data backup
   - Document current configuration
   - Prepare replacement drive

2. **Replacement Steps**:
   - Power down server safely
   - Replace failed drive
   - Restore data from backup
   - Verify system functionality

## Advanced Solutions
1. **RAID Configuration**:
   - Implement RAID for redundancy
   - Configure hot spare drives
   - Monitor RAID health status

2. **Storage Monitoring**:
   - Implement SMART monitoring
   - Set up automated alerts
   - Regular health checks

## Prevention Measures
1. **Regular Maintenance**:
   - Monthly SMART health checks
   - Regular data backups
   - Environmental monitoring

2. **Proactive Replacement**:
   - Replace drives before failure
   - Maintain spare drives
   - Document replacement schedules

## Recovery Planning
- Develop disaster recovery procedures
- Test backup and restore processes
- Maintain emergency contact lists
- Regular recovery testing""",
        "Hardware"
    ),
    (
        "Wireless Access Point Overload Resolution",
        """# High-Density Wi-Fi Overload Solutions

## Network Analysis
1. **Access Point Assessment**:
   - Check AP utilization and client count
   - Identify overloaded access points
   - Analyze coverage patterns

2. **Client Distribution**:
   - Map client locations
   - Identify high-density areas
   - Check for coverage gaps

## Immediate Solutions
1. **Load Balancing**:
   - Configure client load balancing
   - Adjust power levels
   - Enable band steering

2. **Channel Optimization**:
   - Analyze channel utilization
   - Adjust channel assignments
   - Implement channel bonding

## Infrastructure Improvements
1. **Additional Access Points**:
   - Install additional APs in high-density areas
   - Configure proper spacing
   - Implement mesh networking if needed

2. **Capacity Planning**:
   - Calculate required AP density
   - Plan for future growth
   - Implement scalable solutions

## Advanced Solutions
1. **Wi-Fi 6 Implementation**:
   - Upgrade to Wi-Fi 6 access points
   - Configure OFDMA for efficiency
   - Implement BSS coloring

2. **Network Segmentation**:
   - Create separate SSIDs for different use cases
   - Implement VLAN segmentation
   - Configure QoS policies

## Performance Optimization
1. **Bandwidth Management**:
   - Implement bandwidth limits per user
   - Configure traffic shaping
   - Prioritize business applications

2. **Client Management**:
   - Update client drivers
   - Configure power management
   - Implement connection policies

## Monitoring and Maintenance
- Regular performance monitoring
- Capacity planning reviews
- Regular firmware updates
- User experience monitoring""",
        "Network"
    ),
    (
        "SharePoint Document Library Sync Issues",
        """# SharePoint Sync Failure Resolution

## Sync Issue Diagnosis
1. **OneDrive Client Status**:
   - Check OneDrive sync status in system tray
   - Review sync error messages
   - Verify account authentication

2. **Library Analysis**:
   - Check library permissions
   - Verify library size and file count
   - Identify problematic files

## Client-Side Solutions
1. **OneDrive Reset**:
   - Close OneDrive application
   - Clear OneDrive cache
   - Restart OneDrive sync

2. **Account Re-authentication**:
   - Sign out of OneDrive
   - Clear stored credentials
   - Sign back in with fresh credentials

## Advanced Solutions
1. **Selective Sync**:
   - Configure selective sync for large libraries
   - Exclude unnecessary folders
   - Optimize sync performance

2. **Library Optimization**:
   - Break large libraries into smaller ones
   - Implement document versioning policies
   - Configure retention policies

## Server-Side Solutions
1. **SharePoint Health Check**:
   - Verify SharePoint service health
   - Check for service updates
   - Review tenant configuration

2. **Library Configuration**:
   - Optimize library settings
   - Configure proper permissions
   - Implement content types

## Prevention Measures
1. **Best Practices**:
   - Regular library maintenance
   - Proper file naming conventions
   - Regular sync monitoring

2. **User Training**:
   - Train users on sync best practices
   - Provide troubleshooting guides
   - Regular sync health checks

## Advanced Troubleshooting
- Use SharePoint migration tools
- Implement hybrid configurations
- Regular performance monitoring
- Document sync procedures""",
        "Software"
    ),
    (
        "USB Device Sleep Mode Issues",
        """# USB Device Sleep Mode Problems

## Issue Analysis
1. **Power Management Check**:
   - Review USB power management settings
   - Check device power states
   - Identify affected USB devices

2. **Driver Status**:
   - Verify USB device drivers
   - Check for driver conflicts
   - Review device manager status

## Power Management Solutions
1. **USB Power Settings**:
   - Device Manager → Universal Serial Bus controllers
   - Disable "Allow computer to turn off this device"
   - Apply to all USB root hubs

2. **Power Plan Configuration**:
   - Control Panel → Power Options
   - Change plan settings → Advanced
   - Configure USB selective suspend

## Driver Solutions
1. **Driver Updates**:
   - Update USB controller drivers
   - Update chipset drivers
   - Restart after driver updates

2. **Driver Rollback**:
   - Rollback recent driver updates
   - Use system restore if needed
   - Test with different driver versions

## Advanced Solutions
1. **Registry Modifications**:
   - Modify USB power management registry entries
   - Disable USB selective suspend
   - Configure USB power policies

2. **BIOS Configuration**:
   - Check BIOS USB settings
   - Disable USB power saving
   - Enable USB legacy support

## Hardware Solutions
1. **USB Port Testing**:
   - Test different USB ports
   - Check for port damage
   - Use powered USB hubs

2. **Device Replacement**:
   - Test with different devices
   - Replace faulty USB devices
   - Check device compatibility

## Prevention
- Regular driver updates
- Proper power management configuration
- Regular hardware testing
- User training on USB best practices""",
        "Hardware"
    ),
    (
        "Internet Bandwidth Saturation Management",
        """# Corporate Internet Bandwidth Optimization

## Bandwidth Analysis
1. **Traffic Monitoring**:
   - Use network monitoring tools
   - Identify bandwidth-consuming applications
   - Analyze peak usage patterns

2. **User Impact Assessment**:
   - Survey users on performance issues
   - Identify critical business applications
   - Document productivity impact

## Immediate Solutions
1. **Traffic Shaping**:
   - Implement QoS policies
   - Prioritize business applications
   - Limit non-business traffic

2. **Application Control**:
   - Block or limit streaming services
   - Implement download restrictions
   - Configure application policies

## Infrastructure Solutions
1. **Bandwidth Upgrade**:
   - Evaluate current bandwidth needs
   - Plan for bandwidth increase
   - Implement redundant connections

2. **Load Balancing**:
   - Distribute traffic across multiple connections
   - Implement failover mechanisms
   - Configure traffic routing

## Advanced Solutions
1. **SD-WAN Implementation**:
   - Deploy software-defined WAN
   - Optimize application routing
   - Implement dynamic bandwidth allocation

2. **Caching Solutions**:
   - Implement web caching
   - Cache frequently accessed content
   - Reduce bandwidth consumption

## Policy Implementation
1. **Acceptable Use Policy**:
   - Define acceptable internet usage
   - Implement monitoring and enforcement
   - Regular policy reviews

2. **Bandwidth Allocation**:
   - Allocate bandwidth by department
   - Implement fair usage policies
   - Monitor and adjust allocations

## Monitoring and Optimization
- Regular bandwidth monitoring
- Performance trend analysis
- User feedback collection
- Continuous optimization""",
        "Network"
    ),
    (
        "Active Directory Authentication Performance",
        """# Active Directory Login Performance Optimization

## Performance Analysis
1. **Authentication Monitoring**:
   - Monitor domain controller performance
   - Check authentication response times
   - Identify authentication bottlenecks

2. **System Resource Check**:
   - Monitor CPU and memory usage
   - Check disk I/O performance
   - Review network connectivity

## Domain Controller Optimization
1. **Service Optimization**:
   - Restart domain controller services
   - Clear DNS cache on DCs
   - Optimize Active Directory database

2. **Resource Allocation**:
   - Increase domain controller memory
   - Optimize disk performance
   - Configure proper CPU allocation

## Network Solutions
1. **DNS Optimization**:
   - Optimize DNS server configuration
   - Implement DNS caching
   - Configure proper DNS forwarders

2. **Network Connectivity**:
   - Check network latency to DCs
   - Optimize network routing
   - Implement network redundancy

## Advanced Solutions
1. **Active Directory Health**:
   - Run DCDIAG health checks
   - Check replication status
   - Verify FSMO role holders

2. **Group Policy Optimization**:
   - Optimize Group Policy processing
   - Reduce GPO complexity
   - Implement GPO caching

## Client-Side Solutions
1. **Client Configuration**:
   - Optimize client DNS settings
   - Configure proper domain membership
   - Update client drivers

2. **Authentication Caching**:
   - Enable credential caching
   - Configure offline authentication
   - Implement smart card optimization

## Monitoring and Maintenance
- Regular performance monitoring
- Active Directory health checks
- Regular maintenance procedures
- Performance trend analysis""",
        "Software"
    ),
    (
        "General IT Security Best Practices",
        """# IT Security Best Practices Guide

## Password Security
1. **Strong Password Creation**:
   - Use at least 12 characters
   - Include uppercase, lowercase, numbers, symbols
   - Avoid common words and patterns
   - Use unique passwords for each account

2. **Password Management**:
   - Use password manager applications
   - Enable two-factor authentication
   - Regular password updates
   - Never share passwords

## Email Security
1. **Phishing Prevention**:
   - Verify sender identity
   - Check for suspicious links
   - Don't open unexpected attachments
   - Report suspicious emails

2. **Email Best Practices**:
   - Use company email for business only
   - Be cautious with personal information
   - Regular email security training
   - Keep email client updated

## Device Security
1. **Software Updates**:
   - Keep operating system updated
   - Update applications regularly
   - Enable automatic updates
   - Restart systems after updates

2. **Antivirus Protection**:
   - Install and maintain antivirus software
   - Regular virus scans
   - Keep definitions updated
   - Enable real-time protection

## Network Security
1. **Wi-Fi Security**:
   - Use secure Wi-Fi networks
   - Avoid public Wi-Fi for sensitive data
   - Use VPN when necessary
   - Keep Wi-Fi passwords secure

2. **Firewall Configuration**:
   - Enable firewall protection
   - Configure proper rules
   - Regular firewall reviews
   - Monitor firewall logs

## Data Protection
1. **Backup Procedures**:
   - Regular data backups
   - Test backup restoration
   - Store backups securely
   - Document backup procedures

2. **Data Handling**:
   - Encrypt sensitive data
   - Use secure file sharing
   - Proper data disposal
   - Follow data retention policies

## Incident Response
- Report security incidents immediately
- Follow incident response procedures
- Document security events
- Learn from security incidents""",
        "Accounts"
    ),
    (
        "Remote Work IT Support Guide",
        """# Remote Work IT Support Procedures

## Remote Access Setup
1. **VPN Configuration**:
   - Install company VPN client
   - Configure connection settings
   - Test VPN connectivity
   - Troubleshoot connection issues

2. **Remote Desktop Setup**:
   - Configure remote desktop access
   - Set up secure connections
   - Test remote access functionality
   - Document access procedures

## Home Network Optimization
1. **Wi-Fi Configuration**:
   - Optimize home Wi-Fi settings
   - Position router appropriately
   - Use 5GHz band when possible
   - Secure home network

2. **Bandwidth Management**:
   - Monitor internet usage
   - Optimize for work applications
   - Limit non-work traffic during work hours
   - Consider bandwidth upgrades

## Equipment Management
1. **Laptop Setup**:
   - Configure work laptop properly
   - Install required software
   - Set up external monitors
   - Configure ergonomic workspace

2. **Peripheral Devices**:
   - Set up external keyboard and mouse
   - Configure webcam and microphone
   - Test audio/video equipment
   - Troubleshoot device issues

## Software and Applications
1. **Collaboration Tools**:
   - Set up Microsoft Teams
   - Configure video conferencing
   - Test screen sharing
   - Troubleshoot meeting issues

2. **Business Applications**:
   - Install required business software
   - Configure application settings
   - Test application functionality
   - Troubleshoot application issues

## Security Considerations
1. **Home Security**:
   - Secure home Wi-Fi network
   - Use strong passwords
   - Enable network encryption
   - Regular security updates

2. **Data Protection**:
   - Use company-approved devices
   - Follow data handling policies
   - Secure physical workspace
   - Report security concerns

## Troubleshooting Common Issues
- Internet connectivity problems
- VPN connection issues
- Audio/video problems
- Application performance issues
- Security concerns

## Support Procedures
- Contact IT support for assistance
- Document issues thoroughly
- Follow remote support procedures
- Escalate critical issues appropriately""",
        "Network"
    ),
    (
        "IT Asset Management Best Practices",
        """# IT Asset Management Procedures

## Asset Tracking
1. **Inventory Management**:
   - Maintain accurate asset inventory
   - Track asset locations and users
   - Document asset specifications
   - Regular inventory audits

2. **Asset Lifecycle**:
   - Track asset procurement dates
   - Monitor warranty periods
   - Plan for asset replacement
   - Document disposal procedures

## Hardware Management
1. **Computer Management**:
   - Track computer specifications
   - Monitor hardware performance
   - Plan hardware upgrades
   - Manage hardware warranties

2. **Peripheral Management**:
   - Track printers and scanners
   - Monitor peripheral usage
   - Manage peripheral maintenance
   - Plan peripheral replacement

## Software Management
1. **License Tracking**:
   - Maintain software license inventory
   - Track license usage
   - Monitor license expiration dates
   - Plan license renewals

2. **Software Deployment**:
   - Track software installations
   - Monitor software usage
   - Manage software updates
   - Plan software upgrades

## Procurement Procedures
1. **Purchase Requests**:
   - Submit proper purchase requests
   - Justify business need
   - Follow approval procedures
   - Document procurement decisions

2. **Vendor Management**:
   - Maintain vendor relationships
   - Track vendor performance
   - Manage vendor contracts
   - Plan vendor evaluations

## Maintenance and Support
1. **Preventive Maintenance**:
   - Schedule regular maintenance
   - Perform hardware cleaning
   - Update software regularly
   - Monitor system performance

2. **Support Procedures**:
   - Document support requests
   - Track resolution times
   - Monitor support quality
   - Plan support improvements

## Compliance and Security
1. **Asset Security**:
   - Implement asset security policies
   - Track asset access
   - Monitor asset usage
   - Plan security improvements

2. **Compliance Management**:
   - Ensure regulatory compliance
   - Document compliance procedures
   - Regular compliance audits
   - Plan compliance improvements

## Reporting and Analytics
- Generate asset reports
- Analyze asset utilization
- Monitor asset costs
- Plan asset optimization""",
        "Hardware"
    ),
    (
        "Cloud Services Integration Guide",
        """# Cloud Services Integration and Management

## Cloud Strategy Planning
1. **Service Evaluation**:
   - Assess business requirements
   - Evaluate cloud service options
   - Compare costs and benefits
   - Plan migration strategy

2. **Security Considerations**:
   - Evaluate cloud security features
   - Plan data protection measures
   - Configure access controls
   - Monitor security compliance

## Microsoft 365 Integration
1. **Office 365 Setup**:
   - Configure user accounts
   - Set up email and calendar
   - Configure SharePoint sites
   - Implement security policies

2. **Teams Configuration**:
   - Set up team structures
   - Configure meeting policies
   - Implement security settings
   - Train users on features

## Azure Services
1. **Infrastructure Services**:
   - Set up virtual machines
   - Configure storage accounts
   - Implement backup solutions
   - Monitor service health

2. **Application Services**:
   - Deploy web applications
   - Configure databases
   - Implement monitoring
   - Plan scaling strategies

## Google Workspace Integration
1. **G Suite Setup**:
   - Configure user accounts
   - Set up email and calendar
   - Configure Drive and Docs
   - Implement security policies

2. **Collaboration Tools**:
   - Set up Google Meet
   - Configure Chat and Spaces
   - Implement file sharing
   - Train users on features

## AWS Services
1. **Compute Services**:
   - Set up EC2 instances
   - Configure load balancers
   - Implement auto-scaling
   - Monitor performance

2. **Storage Services**:
   - Configure S3 buckets
   - Set up backup solutions
   - Implement data lifecycle
   - Monitor storage usage

## Multi-Cloud Management
1. **Service Integration**:
   - Plan multi-cloud architecture
   - Configure service connections
   - Implement data synchronization
   - Monitor cross-cloud performance

2. **Cost Management**:
   - Monitor cloud spending
   - Optimize resource usage
   - Implement cost controls
   - Plan budget management

## Security and Compliance
1. **Identity Management**:
   - Implement single sign-on
   - Configure multi-factor authentication
   - Manage user access
   - Monitor access patterns

2. **Data Protection**:
   - Implement encryption
   - Configure backup solutions
   - Plan disaster recovery
   - Monitor data compliance

## Monitoring and Optimization
- Monitor service performance
- Track usage patterns
- Optimize resource allocation
- Plan capacity management""",
        "Software"
    )]
articles = [KBArticle(title=t, content=c, category=cat) for (t, c, cat) in kb_items]
db.session.add_all(articles)
db.session.commit()


print("✅ Database seeded successfully with dummy data!")
