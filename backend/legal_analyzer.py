# backend/legal_analyzer.py
import os
import json
import pandas as pd

class LegalAnalyzer:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.setup_analyzer()
    
    def setup_analyzer(self):
        """Setup the legal analyzer without dataset dependency"""
        print("🔧 Setting up Legal Analyzer...")
        
        # Improved legal categories and keywords with more specific terms
        self.legal_keywords = {
            'housing': [
                'landlord', 'tenant', 'rent', 'eviction', 'lease', 'apartment', 'house',
                'security deposit', 'deposit', 'move out', 'moved out', 'rental',
                'housing', 'property manager', 'lease agreement', 'rental agreement',
                'maintenance', 'repair', 'habitable', 'mold', 'pest', 'utilities'
            ],
            'employment': [
                'employer', 'employee', 'wage', 'salary', 'overtime', 'work', 'job', 'fire',
                'terminated', 'paycheck', 'hours', 'shift', 'boss', 'manager', 'workplace',
                'discrimination', 'harassment', 'wrongful termination', 'minimum wage',
                'break', 'lunch', 'vacation', 'benefits', 'hr', 'human resources'
            ],
            'consumer': [
                'buy', 'purchase', 'refund', 'warranty', 'product', 'service', 'contract',
                'defective', 'broken', 'not working', 'scam', 'fraud', 'deceptive',
                'return', 'exchange', 'store', 'merchant', 'seller', 'warranty',
                'guarantee', 'consumer rights', 'false advertising'
            ],
            'family': [
                'divorce', 'marriage', 'child', 'custody', 'support', 'family', 'spouse',
                'visitation', 'parenting time', 'alimony', 'marital', 'separation',
                'child support', 'paternity', 'adoption', 'guardianship'
            ],
            'property': [
                'property', 'house', 'land', 'ownership', 'deed', 'mortgage', 'title',
                'boundary', 'neighbor', 'fence', 'easement', 'zoning', 'real estate'
            ]
        }
        
        print("✅ Legal Analyzer ready!")
    
    def analyze_legal_issue(self, user_input):
        """Analyze user input and provide legal insights"""
        user_input_lower = user_input.lower()
        
        # Determine legal category
        category = self._categorize_issue(user_input_lower)
        
        # Generate specific analysis based on keywords
        analysis = self._generate_specific_analysis(category, user_input_lower)
        
        # Suggest resources
        resources = self._suggest_resources(category)
        
        return {
            'category': category,
            'analysis': analysis,
            'resources': resources,
            'relevant_laws': self._get_relevant_laws(category)
        }
    
    def _categorize_issue(self, text):
        """Categorize the legal issue"""
        for category, keywords in self.legal_keywords.items():
            if any(keyword in text for keyword in keywords):
                return category
        return 'general'
    
    def _generate_specific_analysis(self, category, user_input):
        """Generate specific legal analysis based on keywords in the input"""
        
        # HOUSING SPECIFIC ANALYSES
        if category == 'housing':
            analysis = []
            
            # Security Deposit Issues
            if any(keyword in user_input for keyword in ['security deposit', 'deposit', 'move out', 'moved out']):
                analysis.extend([
                    "Security deposits must be returned within 21-30 days after move-out (varies by state)",
                    "Landlords must provide an itemized written statement of deductions",
                    "Normal wear and tear cannot be charged against your deposit",
                    "If deposit isn't returned on time, you may be entitled to 2-3x the amount in damages",
                    "Take photos/videos of the property condition when moving in and out"
                ])
            
            # Rent Increase Issues
            if any(keyword in user_input for keyword in ['rent increase', 'rent raised']):
                analysis.extend([
                    "Landlords typically need to provide 30-60 days written notice for rent increases",
                    "Rent control laws may limit the percentage or frequency of increases in some areas",
                    "Check your lease agreement for specific terms about rent changes during the lease term"
                ])
            
            # Repair/Maintenance Issues
            if any(keyword in user_input for keyword in ['repair', 'maintenance', 'broken', 'not working', 'mold', 'pest']):
                analysis.extend([
                    "Landlords must maintain habitable living conditions (heat, water, electricity, structural safety)",
                    "You may have the right to repair and deduct if landlord doesn't make essential repairs",
                    "Document all repair requests in writing and keep copies",
                    "In some states, you can withhold rent for serious habitability issues"
                ])
            
            # Eviction Issues
            if 'eviction' in user_input:
                analysis.extend([
                    "Landlords must provide proper written notice before filing for eviction",
                    "Eviction procedures vary by state but typically require court proceedings",
                    "You have the right to contest an eviction in court",
                    "Retaliatory eviction for complaining about conditions may be illegal"
                ])
            
            # Add general housing rights if no specific issues matched
            if not analysis:
                analysis.extend([
                    "Tenants have the right to quiet enjoyment of their rental unit",
                    "Landlords must provide proper notice before entering your unit (usually 24-48 hours)",
                    "You have rights against discrimination based on race, religion, gender, etc.",
                    "Lease agreements must comply with state and local housing laws"
                ])
            
            return analysis
        
        # EMPLOYMENT SPECIFIC ANALYSES
        elif category == 'employment':
            analysis = []
            
            # Wage/Overtime Issues
            if any(keyword in user_input for keyword in ['overtime', 'pay', 'wage', 'salary', 'hours']):
                analysis.extend([
                    "Non-exempt employees must be paid 1.5x regular rate for hours over 40 per week",
                    "Employers must pay at least federal/state minimum wage for all hours worked",
                    "Unauthorized deductions from paychecks are generally prohibited",
                    "Keep detailed records of all hours worked, including overtime"
                ])
            
            # Termination Issues
            if any(keyword in user_input for keyword in ['fire', 'fired', 'terminated', 'laid off']):
                analysis.extend([
                    "Most employment is 'at-will' but wrongful termination laws still apply",
                    "You cannot be fired for discriminatory reasons (race, gender, age, disability, etc.)",
                    "Retaliation for reporting illegal activities (whistleblowing) is prohibited",
                    "You may be entitled to severance pay depending on company policy and circumstances"
                ])
            
            # Discrimination/Harassment
            if any(keyword in user_input for keyword in ['discrimination', 'harassment', 'hostile']):
                analysis.extend([
                    "Employment discrimination based on protected characteristics is illegal under federal law",
                    "You have the right to work in an environment free from harassment",
                    "Document incidents with dates, times, witnesses, and specific details",
                    "File complaints with EEOC or state human rights commission within statutory deadlines"
                ])
            
            if not analysis:
                analysis.extend([
                    "Employees have rights to a safe working environment under OSHA",
                    "You may have rights to family/medical leave for qualified situations",
                    "Employers must provide required breaks and meal periods as per state law",
                    "You have rights regarding your personnel file and employment records"
                ])
            
            return analysis
        
        # CONSUMER SPECIFIC ANALYSES
        elif category == 'consumer':
            analysis = []
            
            # Product Issues
            if any(keyword in user_input for keyword in ['defective', 'broken', 'not working', 'warranty']):
                analysis.extend([
                    "Products must be merchantable and fit for their intended purpose",
                    "Implied warranties may apply even if no written warranty is provided",
                    "You may have rights to repair, replacement, or refund for defective products",
                    "Document the defect with photos and keep all purchase receipts"
                ])
            
            # Refund/Return Issues
            if any(keyword in user_input for keyword in ['refund', 'return', 'exchange']):
                analysis.extend([
                    "Store return policies are generally discretionary unless product is defective",
                    "For defective products, you have stronger rights to refunds or exchanges",
                    "Credit card chargebacks may be an option for undelivered or defective goods",
                    "Keep all communication with the seller in writing"
                ])
            
            # Fraud/Scam Issues
            if any(keyword in user_input for keyword in ['scam', 'fraud', 'deceptive']):
                analysis.extend([
                    "Deceptive business practices and false advertising are illegal",
                    "You may have rights under consumer protection laws for fraudulent transactions",
                    "Report scams to your state attorney general and consumer protection agencies",
                    "Credit card companies may help with fraudulent charges"
                ])
            
            if not analysis:
                analysis.extend([
                    "Consumer protection laws require honest business practices and advertising",
                    "You have rights to cancel certain contracts within cooling-off periods",
                    "Debt collection practices are regulated by federal and state laws",
                    "Keep records of all transactions and communications with businesses"
                ])
            
            return analysis
        
        # FAMILY LAW SPECIFIC ANALYSES
        elif category == 'family':
            analysis = []
            
            # Divorce Issues
            if any(keyword in user_input for keyword in ['divorce', 'separation', 'marital']):
                analysis.extend([
                    "Divorce procedures vary by state (fault vs. no-fault)",
                    "Marital property is typically divided equitably or equally depending on state",
                    "Temporary support orders may be available during divorce proceedings",
                    "Consider mediation as an alternative to litigation"
                ])
            
            # Child Custody/Support
            if any(keyword in user_input for keyword in ['custody', 'child support', 'visitation', 'parenting']):
                analysis.extend([
                    "Child custody decisions are based on the best interests of the child",
                    "Courts generally encourage shared parenting when safe and appropriate",
                    "Child support amounts follow state guidelines based on income and expenses",
                    "Custody and support orders can be modified with changed circumstances"
                ])
            
            if not analysis:
                analysis.extend([
                    "Family law matters often benefit from mediation and collaborative approaches",
                    "Legal separation may be an alternative to divorce in some situations",
                    "Prenuptial and postnuptial agreements can define property rights",
                    "Grandparents may have visitation rights in certain circumstances"
                ])
            
            return analysis
        
        # GENERAL ANALYSIS (fallback)
        else:
            return [
                "Document all relevant details, dates, and communications related to your situation",
                "Statutes of limitations may apply, so consider acting promptly to preserve your rights",
                "Consult with a qualified attorney in your jurisdiction for specific legal advice",
                "Keep records of all evidence, including photos, documents, and correspondence"
            ]
    
    def _suggest_resources(self, category):
        """Suggest appropriate legal resources"""
        resources = {
            'housing': [
                "Local Tenant Union or Housing Advocacy Group",
                "State Housing Authority or Attorney General's Office", 
                "Legal Aid Society - Housing Law Division",
                "Local Bar Association Lawyer Referral Service"
            ],
            'employment': [
                "U.S. Department of Labor - Wage and Hour Division",
                "Equal Employment Opportunity Commission (EEOC)",
                "State Labor Department or Workforce Agency",
                "Employment Law Attorney specializing in your issue"
            ],
            'consumer': [
                "State Consumer Protection Agency",
                "Better Business Bureau",
                "Federal Trade Commission (FTC)",
                "State Attorney General's Consumer Protection Division"
            ],
            'family': [
                "Family Law Attorney with relevant experience",
                "Mediation and Collaborative Law Services",
                "Local Family Court Self-Help Center",
                "Child Support Enforcement Agency"
            ],
            'general': [
                "Local Bar Association Lawyer Referral Service",
                "Legal Aid Organization in your area",
                "Law School Legal Clinic",
                "State Court Self-Help Resources"
            ]
        }
        
        return resources.get(category, resources['general'])
    
    def _get_relevant_laws(self, category):
        """Get relevant laws for the category"""
        laws = {
            'housing': [
                "Fair Housing Act",
                "State Landlord-Tenant Laws", 
                "Implied Warranty of Habitability",
                "Security Deposit Statutes"
            ],
            'employment': [
                "Fair Labor Standards Act (FLSA)",
                "Title VII of Civil Rights Act",
                "Americans with Disabilities Act (ADA)",
                "State Wage and Hour Laws"
            ],
            'consumer': [
                "Consumer Protection Act",
                "Magnuson-Moss Warranty Act", 
                "Uniform Commercial Code",
                "State Consumer Fraud Acts"
            ],
            'family': [
                "State Family Law Acts",
                "Child Support Guidelines", 
                "Uniform Child Custody Jurisdiction Act",
                "Domestic Relations Laws"
            ]
        }
        
        return laws.get(category, ["General Legal Principles", "State-Specific Regulations"])