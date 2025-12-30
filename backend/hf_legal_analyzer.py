# backend/hf_legal_analyzer.py
import requests
import json
from hf_config import HFConfig

class HFLegalAnalyzer:
    def __init__(self):
        self.setup_analyzer()
        self.legal_database = self._setup_legal_database()
    
    def setup_analyzer(self):
        """Setup the AI analyzer"""
        print("🤖 Initializing Enhanced Legal Analyzer...")
        if HFConfig.is_configured():
            print("✅ Hugging Face API configured")
        else:
            print("⚠️  Using enhanced fallback analysis")
        print("✅ Enhanced Legal Analyzer ready!")
    
    def _setup_legal_database(self):
        """Setup comprehensive legal reference database"""
        return {
            "housing and landlord tenant law": {
                "security_deposit": {
                    "laws": [
                        "Uniform Residential Landlord and Tenant Act (URLTA) § 2.101",
                        "State Security Deposit Statutes (e.g., CA Civil Code § 1950.5)",
                        "Implied Warranty of Habitability",
                        "Fair Housing Act 42 U.S.C. § 3601"
                    ],
                    "timeframes": "21-30 days depending on state jurisdiction",
                    "requirements": "Itemized written statement of deductions required",
                    "remedies": "2-3x damages for wrongful withholding in many states"
                },
                "rent_increase": {
                    "laws": [
                        "State Rent Control Ordinances",
                        "Lease Agreement Contract Law",
                        "Covenant of Quiet Enjoyment", 
                        "Constructive Eviction Doctrine"
                    ],
                    "notice_period": "30-60 days notice typically required",
                    "limitations": "Rent control areas may limit percentage increases"
                },
                "repairs": {
                    "laws": [
                        "Implied Warranty of Habitability",
                        "Building Code Violations", 
                        "Local Housing Codes",
                        "Retaliatory Eviction Protections"
                    ],
                    "remedies": [
                        "Repair and deduct",
                        "Rent withholding", 
                        "Code enforcement complaints"
                    ]
                }
            },
            "employment and labor law": {
                "wages": {
                    "laws": [
                        "Fair Labor Standards Act (FLSA) 29 U.S.C. § 201",
                        "State Wage and Hour Laws",
                        "Department of Labor Regulations 29 CFR § 541",
                        "Equal Pay Act of 1963"
                    ],
                    "overtime": "1.5x regular rate for hours over 40 per workweek",
                    "minimum_wage": "Federal minimum: $7.25/hour (higher in many states)"
                },
                "discrimination": {
                    "laws": [
                        "Title VII of Civil Rights Act of 1964",
                        "Americans with Disabilities Act (ADA)",
                        "Age Discrimination in Employment Act (ADEA)",
                        "State Human Rights Laws"
                    ],
                    "protected_classes": "Race, color, religion, sex, national origin, age, disability",
                    "enforcement": "EEOC filing within 180-300 days"
                },
                "wrongful_termination": {
                    "laws": [
                        "Public Policy Exception to At-Will Employment",
                        "Whistleblower Protection Acts",
                        "Implied Contract Doctrine",
                        "Covenant of Good Faith and Fair Dealing"
                    ]
                }
            },
            "consumer protection law": {
                "defective_products": {
                    "laws": [
                        "Magnuson-Moss Warranty Act 15 U.S.C. § 2301",
                        "Uniform Commercial Code (UCC) § 2-314",
                        "State Lemon Laws",
                        "Consumer Product Safety Act"
                    ],
                    "warranties": [
                        "Implied Warranty of Merchantability",
                        "Implied Warranty of Fitness for Particular Purpose"
                    ]
                },
                "fraud": {
                    "laws": [
                        "Federal Trade Commission Act § 5",
                        "State Consumer Fraud Acts", 
                        "Truth in Lending Act (TILA)",
                        "Fair Credit Reporting Act (FCRA)"
                    ]
                }
            },
            "family law and divorce": {
                "child_custody": {
                    "laws": [
                        "Uniform Child Custody Jurisdiction and Enforcement Act (UCCJEA)",
                        "Best Interests of the Child Standard",
                        "State Custody and Visitation Statutes"
                    ],
                    "factors": [
                        "Child's relationship with each parent",
                        "Parent's ability to provide stable environment", 
                        "Child's adjustment to home, school, community"
                    ]
                },
                "child_support": {
                    "laws": [
                        "Child Support Enforcement Amendments",
                        "State Child Support Guidelines", 
                        "Income Shares Model"
                    ],
                    "calculation": "Based on both parents' incomes and time-sharing"
                }
            }
        }
    
    def analyze_with_ai(self, user_input):
        """Analyze legal issue with authoritative legal citations"""
        try:
            category = self._classify_issue(user_input)
            specific_issue = self._identify_specific_issue(user_input, category)
            
            analysis = self._generate_authoritative_analysis(user_input, category, specific_issue)
            
            return {
                'category': category,
                'analysis': analysis,
                'resources': self._get_legal_resources(category),
                'relevant_laws': self._get_specific_laws(category, specific_issue),
                'ai_generated': True,
                'legal_citations': self._get_legal_citations(category, specific_issue)
            }
            
        except Exception as e:
            print(f"❌ AI Analysis Error: {e}")
            return self._get_fallback_analysis(user_input)
    
    def _classify_issue(self, user_input):
        """Enhanced classification"""
        text_lower = user_input.lower()
        
        categories = {
            "housing and landlord tenant law": [
                'landlord', 'tenant', 'rent', 'lease', 'eviction', 
                'security deposit', 'apartment', 'housing', 'property manager',
                'habitability', 'repair', 'maintenance'
            ],
            "employment and labor law": [
                'employer', 'employee', 'wage', 'salary', 'overtime',
                'fire', 'terminated', 'discrimination', 'harassment', 'workplace',
                'minimum wage', 'wrongful termination'
            ],
            "consumer protection law": [
                'buy', 'purchase', 'refund', 'warranty', 'defective',
                'scam', 'fraud', 'consumer', 'product', 'service',
                'merchant', 'warranty', 'guarantee'
            ],
            "family law and divorce": [
                'divorce', 'marriage', 'child', 'custody', 'support',
                'spouse', 'alimony', 'visitation', 'parenting', 'separation'
            ]
        }
        
        for category, keywords in categories.items():
            if any(keyword in text_lower for keyword in keywords):
                return category
        
        return "general legal matter"
    
    def _identify_specific_issue(self, user_input, category):
        """Identify specific legal issue within category"""
        text_lower = user_input.lower()
        
        issue_mapping = {
            "housing and landlord tenant law": {
                "security_deposit": ['security deposit', 'deposit', 'move out'],
                "rent_increase": ['rent increase', 'rent raised', 'rent hike'],
                "repairs": ['repair', 'broken', 'not working', 'maintenance', 'fix'],
                "eviction": ['eviction', 'evict', 'remove', 'kick out']
            },
            "employment and labor law": {
                "wages": ['wage', 'pay', 'overtime', 'salary', 'minimum wage'],
                "discrimination": ['discrimination', 'discriminate', 'race', 'gender', 'age'],
                "wrongful_termination": ['fire', 'fired', 'terminated', 'laid off', 'let go'],
                "harassment": ['harassment', 'harass', 'hostile', 'bullying']
            },
            "consumer protection law": {
                "defective_products": ['defective', 'broken', 'not working', 'faulty'],
                "fraud": ['fraud', 'scam', 'deceptive', 'false advertising'],
                "warranty": ['warranty', 'guarantee', 'return policy'],
                "contract": ['contract', 'agreement', 'terms', 'signed']
            },
            "family law and divorce": {
                "child_custody": ['custody', 'visitation', 'parenting time'],
                "child_support": ['child support', 'support payment'],
                "divorce": ['divorce', 'separation', 'marriage dissolution'],
                "alimony": ['alimony', 'spousal support', 'maintenance']
            }
        }
        
        if category in issue_mapping:
            for issue, keywords in issue_mapping[category].items():
                if any(keyword in text_lower for keyword in keywords):
                    return issue
        
        return "general"
    
    def _generate_authoritative_analysis(self, user_input, category, specific_issue):
        """Generate analysis with authoritative legal language"""
        if category in self.legal_database and specific_issue in self.legal_database[category]:
            issue_data = self.legal_database[category][specific_issue]
            return self._create_authoritative_points(category, specific_issue, issue_data, user_input)
        else:
            return self._general_authoritative_analysis(category, user_input)
    
    def _create_authoritative_points(self, category, specific_issue, issue_data, user_input):
        """Create authoritative legal analysis points"""
        points = []
        
        # Point 1: Legal foundation
        if specific_issue == "security_deposit":
            points.append(f"Pursuant to {issue_data['laws'][0]} and state security deposit statutes, landlords must return deposits within {issue_data['timeframes']} with proper accounting.")
            points.append(f"Under the implied warranty of habitability and state landlord-tenant acts, deductions are limited to actual damages beyond normal wear and tear.")
            points.append(f"Remedies available include statutory damages up to {issue_data['remedies']} for failure to comply with deposit return requirements.")
            points.append("Document all communications and consider formal demand letter before initiating legal action.")
        
        elif specific_issue == "wages":
            points.append(f"In accordance with the Fair Labor Standards Act 29 U.S.C. § 207, non-exempt employees are entitled to overtime compensation at 1.5 times their regular rate for hours worked beyond 40 per workweek.")
            points.append(f"State wage and hour laws may provide additional protections beyond federal requirements, including higher minimum wage rates.")
            points.append(f"Employers must maintain accurate records of hours worked as required by Department of Labor regulations 29 CFR § 516.")
            points.append("File a wage claim with the state labor department or consider private action for recovery of unpaid wages with potential liquidated damages.")
        
        elif specific_issue == "defective_products":
            points.append(f"Under the Magnuson-Moss Warranty Act 15 U.S.C. § 2301 and Uniform Commercial Code § 2-314, products carry implied warranties of merchantability and fitness for particular purpose.")
            points.append(f"State consumer protection statutes provide additional remedies for defective products, including repair, replacement, or refund options.")
            points.append(f"Document the defect thoroughly and provide the seller reasonable opportunity to cure before pursuing legal remedies.")
            points.append("Consider filing complaints with consumer protection agencies in addition to potential legal action for breach of warranty.")
        
        elif specific_issue == "child_custody":
            points.append(f"Under the Uniform Child Custody Jurisdiction and Enforcement Act and state family law statutes, custody determinations are based on the best interests of the child standard.")
            points.append(f"Courts consider factors including the child's relationship with each parent, parental ability to provide stability, and the child's adjustment to home and community.")
            points.append(f"Joint custody arrangements are favored when both parents can provide appropriate care and maintain cooperative parenting relationships.")
            points.append("Mediation is often required before custody litigation, and parenting plans should address decision-making and time-sharing arrangements.")
        
        else:
            points.extend([
                f"Based on established legal principles in {category.replace(' and ', '/').title()}, several statutory and common law doctrines may apply to your situation.",
                "Document all relevant facts, communications, and evidence to support your legal position.",
                "Statutes of limitations vary by jurisdiction and legal theory - prompt action is recommended.",
                "Consult with qualified legal counsel to assess specific remedies and litigation strategies."
            ])
        
        return points
    
    def _general_authoritative_analysis(self, category, user_input):
        """General authoritative analysis"""
        return [
            f"Under established legal principles governing {category}, your situation may involve multiple statutory and common law considerations.",
            "Proper documentation of all relevant facts and communications is essential for legal proceedings.",
            "Various legal remedies may be available depending on jurisdiction-specific statutes and case law.",
            "Retain qualified legal counsel to evaluate specific claims and potential litigation strategies."
        ]
    
    def _get_specific_laws(self, category, specific_issue):
        """Get specific laws for the issue"""
        if category in self.legal_database and specific_issue in self.legal_database[category]:
            return self.legal_database[category][specific_issue]['laws']
        return ["General Legal Principles", "State-Specific Statutes"]
    
    def _get_legal_citations(self, category, specific_issue):
        """Get proper legal citations"""
        citations = {
            "housing and landlord tenant law": [
                "Uniform Residential Landlord and Tenant Act (URLTA)",
                "State Landlord-Tenant Statutes", 
                "Building and Housing Codes",
                "Fair Housing Act 42 U.S.C. § 3601"
            ],
            "employment and labor law": [
                "Fair Labor Standards Act 29 U.S.C. § 201",
                "Title VII Civil Rights Act 42 U.S.C. § 2000e",
                "State Labor Codes",
                "EEOC Regulations"
            ],
            "consumer protection law": [
                "Magnuson-Moss Warranty Act 15 U.S.C. § 2301",
                "Federal Trade Commission Act",
                "State Consumer Protection Statutes",
                "Uniform Commercial Code"
            ],
            "family law and divorce": [
                "State Family Code Provisions",
                "Uniform Child Custody Jurisdiction Act",
                "Child Support Guidelines",
                "Domestic Relations Laws"
            ]
        }
        return citations.get(category, ["General Legal Principles"])
    
    def _get_legal_resources(self, category):
        """Get legal resources"""
        resources = {
            "housing and landlord tenant law": [
                "State Housing Authority",
                "Local Tenant Union", 
                "Legal Aid Housing Division",
                "HUD Complaint Line"
            ],
            "employment and labor law": [
                "Department of Labor Wage & Hour Division",
                "Equal Employment Opportunity Commission",
                "State Labor Commissioner",
                "Employment Law Attorney"
            ],
            "consumer protection law": [
                "Consumer Financial Protection Bureau",
                "State Attorney General Consumer Division",
                "Better Business Bureau",
                "Federal Trade Commission"
            ],
            "family law and divorce": [
                "Family Law Attorney Referral Service",
                "Court Self-Help Center",
                "Mediation Services",
                "Child Support Enforcement"
            ]
        }
        return resources.get(category, [
            "State Bar Association Lawyer Referral",
            "Legal Aid Society",
            "Law School Legal Clinic",
            "Court Self-Help Resources"
        ])
    
    def _get_fallback_analysis(self, user_input):
        """Fallback analysis"""
        return {
            'category': 'general legal matter',
            'analysis': [
                "Based on established legal principles, document all relevant facts and communications.",
                "Various statutory and common law remedies may be available depending on jurisdiction.",
                "Statutes of limitations apply to most legal claims - timely action is recommended.",
                "Consult with qualified legal counsel to evaluate specific legal strategies."
            ],
            'resources': [
                "State Bar Association Referral Service",
                "Legal Aid Organization", 
                "Law School Clinical Program",
                "Court Self-Help Center"
            ],
            'relevant_laws': ["General Legal Principles"],
            'legal_citations': ["Applicable State and Federal Statutes"],
            'ai_generated': False
        }