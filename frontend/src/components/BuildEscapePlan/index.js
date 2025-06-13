import React, { useState, useEffect } from 'react';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL;

const BuildEscapePlan = () => {
  const [currentStep, setCurrentStep] = useState(1);
  const [formData, setFormData] = useState({
    // Step 1: Income Type
    incomeType: 'w2',
    
    // Step 2: Business Partner Logic (conditional)
    hasBusinessPartner: false,
    partnerStructure: '',
    
    // Step 3: Capital to Allocate
    annualIncome: '',
    capitalToAllocate: '',
    
    // Step 4: Restructure % Field
    restructurePercentage: '',
    
    // Step 5: Strategy Goal Selection
    primaryGoals: [],
    timeframe: 'short-term',
    
    // Step 6: Forecast Settings
    forecastTimeHorizon: 10,
    returnRate: 6,
    reinvestTaxSavings: true,
    
    // Step 7: Entity Review
    currentEntityStructure: '',
    hasStockCompensation: false,
    stockCompValue: '',
    
    // Step 8: Financial Summary (calculated)
    currentTaxBill: 0,
    projectedSavings: 0,
    
    // Step 9: Strategy Recommendations (generated)
    selectedStrategies: []
  });

  const [forecastData, setForecastData] = useState(null);
  const [strategies, setStrategies] = useState({
    setup: [],
    deductions: [],
    exit: []
  });
  const [implementationStatus, setImplementationStatus] = useState({});
  const [loading, setLoading] = useState(false);
  const [glossaryTerms, setGlossaryTerms] = useState([]);

  useEffect(() => {
    fetchGlossaryTerms();
  }, []);

  const fetchGlossaryTerms = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/glossary`);
      if (response.ok) {
        const terms = await response.json();
        setGlossaryTerms(terms);
      }
    } catch (error) {
      console.error('Failed to load glossary terms:', error);
    }
  };

  // Utility function to format numbers with commas
  const formatNumber = (num) => {
    if (!num) return '';
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  };

  // Utility function to parse comma-formatted numbers
  const parseFormattedNumber = (value) => {
    return parseFloat(value.replace(/,/g, '')) || 0;
  };

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    
    if (name === 'annualIncome' || name === 'capitalToAllocate' || name === 'stockCompValue') {
      // Handle comma-formatted number inputs
      const numericValue = value.replace(/[^\d]/g, '');
      setFormData(prev => ({
        ...prev,
        [name]: formatNumber(numericValue)
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: type === 'checkbox' ? checked : value
      }));
    }
  };

  const handleGoalChange = (goal) => {
    setFormData(prev => ({
      ...prev,
      primaryGoals: prev.primaryGoals.includes(goal) 
        ? prev.primaryGoals.filter(g => g !== goal)
        : [...prev.primaryGoals, goal]
    }));
  };

  const handleStrategyStatusChange = (strategyId, status) => {
    setImplementationStatus(prev => ({
      ...prev,
      [strategyId]: status
    }));
  };

  // Navigation functions
  const nextStep = () => {
    if (currentStep < 9) {
      setCurrentStep(currentStep + 1);
    }
  };

  const prevStep = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const goToStep = (step) => {
    setCurrentStep(step);
  };

  // Strategy Generation Logic
  const generateStrategies = () => {
    const allStrategies = {
      setup: [
        {
          id: 'scorp',
          title: 'S-Corp Election',
          description: 'Reduce self-employment tax through entity optimization',
          complexity: 'Beginner',
          applicableIncome: ['business', 'self-employed'],
          minIncome: 50000,
          maxSavings: 15000,
          glossaryTerm: 'S-Corp Election',
          moduleLink: 'Business Module 1: Entity Structuring'
        },
        {
          id: 'ccorp_mso',
          title: 'C-Corp MSO Structure',
          description: 'Capture income at 21% corporate rate vs 37%+ personal rates',
          complexity: 'Advanced',
          applicableIncome: ['business', 'mixed'],
          minIncome: 500000,
          maxSavings: 80000,
          glossaryTerm: 'MSO (Management Services Organization)',
          moduleLink: 'Business Module 1: Entity Structuring'
        }
      ],
      deductions: [
        {
          id: 'defined_benefit',
          title: 'Defined Benefit Plan',
          description: 'Maximize retirement contributions up to $330K annually',
          complexity: 'Advanced',
          applicableIncome: ['business', 'self-employed'],
          minIncome: 200000,
          maxSavings: 100000,
          glossaryTerm: 'Defined Benefit Plan',
          moduleLink: 'Business Module 3: Strategic Deductions'
        },
        {
          id: 'cost_segregation',
          title: 'Cost Segregation Study',
          description: 'Accelerate depreciation on real estate investments',
          complexity: 'Intermediate',
          applicableIncome: ['investor', 'business'],
          minIncome: 150000,
          maxSavings: 75000,
          glossaryTerm: 'Cost Segregation (Cost Seg)',
          moduleLink: 'W-2 Module 6: Short-Term Rentals'
        }
      ],
      exit: [
        {
          id: 'qsbs',
          title: 'QSBS Qualification',
          description: 'Exclude up to $10M+ in capital gains at business exit',
          complexity: 'Advanced',
          applicableIncome: ['business'],
          minIncome: 200000,
          maxSavings: 2000000,
          glossaryTerm: 'QSBS (Qualified Small Business Stock)',
          moduleLink: 'Business Module 3: Long-Term Wealth Creation'
        }
      ]
    };

    // Filter strategies based on user profile
    const applicableStrategies = {};
    
    Object.keys(allStrategies).forEach(category => {
      applicableStrategies[category] = allStrategies[category].filter(strategy => {
        const incomeCheck = strategy.applicableIncome.includes(formData.incomeType);
        const minIncomeCheck = !formData.annualIncome || parseFormattedNumber(formData.annualIncome) >= strategy.minIncome;
        return incomeCheck && minIncomeCheck;
      });
    });

    return applicableStrategies;
  };

  // Step Progress Indicator
  const renderStepProgress = () => (
    <div className="mb-8">
      <div className="flex items-center justify-center space-x-2">
        {[1, 2, 3, 4, 5, 6, 7, 8, 9].map((step) => (
          <div key={step} className="flex items-center">
            <div
              onClick={() => goToStep(step)}
              className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold cursor-pointer transition-all duration-200 ${
                currentStep === step
                  ? 'bg-emerald-500 text-white'
                  : currentStep > step
                  ? 'bg-emerald-200 text-emerald-700'
                  : 'bg-gray-200 text-gray-500'
              }`}
            >
              {step}
            </div>
            {step < 9 && (
              <div className={`w-8 h-1 ${currentStep > step ? 'bg-emerald-200' : 'bg-gray-200'}`}></div>
            )}
          </div>
        ))}
      </div>
      <div className="text-center mt-4 text-sm text-gray-600">
        Step {currentStep} of 9
      </div>
    </div>
  );

  // Step 1: Income Type Selection
  const renderStep1 = () => (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-navy-900 mb-4">
          Step 1: Income Type
        </h1>
        <p className="text-xl text-gray-600">
          Let's start by understanding your primary income structure
        </p>
      </div>

      <div className="bg-white rounded-xl shadow-lg p-8">
        <h2 className="text-2xl font-bold text-navy-900 mb-6">What's your primary income type?</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {[
            {
              value: 'w2',
              title: 'W-2 Employee',
              description: 'Primary income from employment, stock compensation, bonuses',
              icon: '👔'
            },
            {
              value: 'mixed',
              title: 'Mixed Income',
              description: 'Combination of W-2 and business/investment income',
              icon: '📊'
            },
            {
              value: 'business',
              title: 'Business Owner',
              description: 'Primary income from business ownership, K-1s, self-employment',
              icon: '🏢'
            }
          ].map((option) => (
            <div
              key={option.value}
              onClick={() => setFormData(prev => ({ ...prev, incomeType: option.value }))}
              className={`p-6 border-2 rounded-lg cursor-pointer transition-all duration-200 ${
                formData.incomeType === option.value
                  ? 'border-emerald-500 bg-emerald-50'
                  : 'border-gray-200 hover:border-emerald-300'
              }`}
            >
              <div className="text-center">
                <div className="text-4xl mb-4">{option.icon}</div>
                <h3 className="text-lg font-bold text-navy-900 mb-2">{option.title}</h3>
                <p className="text-sm text-gray-600">{option.description}</p>
              </div>
            </div>
          ))}
        </div>

        <div className="flex justify-end mt-8">
          <button
            onClick={nextStep}
            disabled={!formData.incomeType}
            className={`px-8 py-3 rounded-lg font-bold transition-all duration-200 ${
              formData.incomeType
                ? 'bg-emerald-500 hover:bg-emerald-600 text-white'
                : 'bg-gray-300 text-gray-500 cursor-not-allowed'
            }`}
          >
            Continue →
          </button>
        </div>
      </div>
    </div>
  );

  // Step 2: Business Partner Logic (conditional)
  const renderStep2 = () => {
    // Skip this step for W-2 only income
    if (formData.incomeType === 'w2') {
      React.useEffect(() => {
        nextStep();
      }, []);
      return null;
    }

    return (
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-navy-900 mb-4">
            Step 2: Business Structure
          </h1>
          <p className="text-xl text-gray-600">
            Tell us about your business ownership structure
          </p>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-8">
          <h2 className="text-2xl font-bold text-navy-900 mb-6">Do you have business partners?</h2>
          
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div
                onClick={() => setFormData(prev => ({ ...prev, hasBusinessPartner: false }))}
                className={`p-6 border-2 rounded-lg cursor-pointer transition-all duration-200 ${
                  formData.hasBusinessPartner === false
                    ? 'border-emerald-500 bg-emerald-50'
                    : 'border-gray-200 hover:border-emerald-300'
                }`}
              >
                <h3 className="text-lg font-bold text-navy-900 mb-2">Solo Owner</h3>
                <p className="text-sm text-gray-600">Single owner or family-controlled business</p>
              </div>
              
              <div
                onClick={() => setFormData(prev => ({ ...prev, hasBusinessPartner: true }))}
                className={`p-6 border-2 rounded-lg cursor-pointer transition-all duration-200 ${
                  formData.hasBusinessPartner === true
                    ? 'border-emerald-500 bg-emerald-50'
                    : 'border-gray-200 hover:border-emerald-300'
                }`}
              >
                <h3 className="text-lg font-bold text-navy-900 mb-2">Multiple Partners</h3>
                <p className="text-sm text-gray-600">Business with multiple owners or partners</p>
              </div>
            </div>

            {formData.hasBusinessPartner && (
              <div className="mt-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Current Partnership Structure
                </label>
                <select
                  name="partnerStructure"
                  value={formData.partnerStructure}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                >
                  <option value="">Select structure</option>
                  <option value="equal-partners">Equal partners</option>
                  <option value="majority-minority">Majority/minority structure</option>
                  <option value="silent-partners">Silent partners</option>
                  <option value="family-business">Family business</option>
                  <option value="other">Other</option>
                </select>
              </div>
            )}
          </div>

          <div className="flex justify-between mt-8">
            <button
              onClick={prevStep}
              className="px-6 py-3 border border-gray-300 rounded-lg font-medium text-gray-700 hover:bg-gray-50"
            >
              ← Previous
            </button>
            <button
              onClick={nextStep}
              disabled={formData.hasBusinessPartner === null || (formData.hasBusinessPartner && !formData.partnerStructure)}
              className={`px-8 py-3 rounded-lg font-bold transition-all duration-200 ${
                (formData.hasBusinessPartner !== null && (!formData.hasBusinessPartner || formData.partnerStructure))
                  ? 'bg-emerald-500 hover:bg-emerald-600 text-white'
                  : 'bg-gray-300 text-gray-500 cursor-not-allowed'
              }`}
            >
              Continue →
            </button>
          </div>
        </div>
      </div>
    );
  };

  // Step 3: Capital to Allocate
  const renderStep3 = () => (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-navy-900 mb-4">
          Step 3: Financial Profile
        </h1>
        <p className="text-xl text-gray-600">
          Help us understand your income and investment capacity
        </p>
      </div>

      <div className="bg-white rounded-xl shadow-lg p-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Annual Income *
            </label>
            <div className="relative">
              <span className="absolute left-3 top-3 text-gray-500">$</span>
              <input
                type="text"
                name="annualIncome"
                value={formData.annualIncome}
                onChange={handleInputChange}
                placeholder="250,000"
                className="w-full pl-8 pr-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
              />
            </div>
            <p className="text-xs text-gray-500 mt-1">Enter your total annual income before taxes</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Capital to Allocate *
            </label>
            <div className="relative">
              <span className="absolute left-3 top-3 text-gray-500">$</span>
              <input
                type="text"
                name="capitalToAllocate"
                value={formData.capitalToAllocate}
                onChange={handleInputChange}
                placeholder="50,000"
                className="w-full pl-8 pr-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
              />
            </div>
            <p className="text-xs text-gray-500 mt-1">Amount available for tax strategies and investments</p>
          </div>
        </div>

        {/* Stock Compensation Question for W-2 earners */}
        {formData.incomeType === 'w2' && (
          <div className="mt-8 p-6 bg-blue-50 border border-blue-200 rounded-lg">
            <h3 className="text-lg font-bold text-navy-900 mb-4">Stock Compensation</h3>
            
            <div className="flex items-center mb-4">
              <input
                type="checkbox"
                name="hasStockCompensation"
                checked={formData.hasStockCompensation}
                onChange={handleInputChange}
                className="h-4 w-4 text-emerald-600 focus:ring-emerald-500 border-gray-300 rounded"
              />
              <label className="ml-3 text-sm text-gray-700">
                I receive stock compensation (RSUs, Stock Options, ESPP)
              </label>
            </div>

            {formData.hasStockCompensation && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Annual Stock Compensation Value
                </label>
                <div className="relative">
                  <span className="absolute left-3 top-3 text-gray-500">$</span>
                  <input
                    type="text"
                    name="stockCompValue"
                    value={formData.stockCompValue}
                    onChange={handleInputChange}
                    placeholder="100,000"
                    className="w-full pl-8 pr-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                  />
                </div>
                <p className="text-xs text-gray-500 mt-1">Estimated annual value of stock grants and options</p>
              </div>
            )}
          </div>
        )}

        <div className="flex justify-between mt-8">
          <button
            onClick={prevStep}
            className="px-6 py-3 border border-gray-300 rounded-lg font-medium text-gray-700 hover:bg-gray-50"
          >
            ← Previous
          </button>
          <button
            onClick={nextStep}
            disabled={!formData.annualIncome || !formData.capitalToAllocate}
            className={`px-8 py-3 rounded-lg font-bold transition-all duration-200 ${
              formData.annualIncome && formData.capitalToAllocate
                ? 'bg-emerald-500 hover:bg-emerald-600 text-white'
                : 'bg-gray-300 text-gray-500 cursor-not-allowed'
            }`}
          >
            Continue →
          </button>
        </div>
      </div>
    </div>
  );

  // Step 4: Restructure % Field
  const renderStep4 = () => (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-navy-900 mb-4">
          Step 4: Restructure Planning
        </h1>
        <p className="text-xl text-gray-600">
          What percentage of your financial structure are you willing to optimize?
        </p>
      </div>

      <div className="bg-white rounded-xl shadow-lg p-8">
        <h2 className="text-2xl font-bold text-navy-900 mb-6">Restructure Percentage</h2>
        
        <div className="max-w-md mx-auto">
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-4">
              What percentage of your income/assets are you open to restructuring for tax optimization?
            </label>
            
            <div className="relative">
              <input
                type="number"
                name="restructurePercentage"
                value={formData.restructurePercentage}
                onChange={handleInputChange}
                min="0"
                max="100"
                placeholder="25"
                className="w-full px-4 py-3 pr-8 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 text-center text-xl font-bold"
              />
              <span className="absolute right-3 top-3 text-gray-500 text-xl">%</span>
            </div>
          </div>

          {/* Visual slider */}
          <div className="mb-8">
            <input
              type="range"
              name="restructurePercentage"
              value={formData.restructurePercentage || 0}
              onChange={handleInputChange}
              min="0"
              max="100"
              step="5"
              className="w-full h-3 bg-gray-200 rounded-lg appearance-none cursor-pointer"
              style={{
                background: `linear-gradient(to right, #10b981 0%, #10b981 ${formData.restructurePercentage || 0}%, #e5e7eb ${formData.restructurePercentage || 0}%, #e5e7eb 100%)`
              }}
            />
            <div className="flex justify-between text-xs text-gray-500 mt-2">
              <span>0% (Conservative)</span>
              <span>50% (Moderate)</span>
              <span>100% (Aggressive)</span>
            </div>
          </div>

          {/* Guidance based on percentage */}
          <div className="bg-gray-50 rounded-lg p-4">
            <h3 className="font-bold text-gray-900 mb-2">
              {formData.restructurePercentage >= 75 ? 'Aggressive Approach' :
               formData.restructurePercentage >= 50 ? 'Balanced Approach' :
               formData.restructurePercentage >= 25 ? 'Conservative Approach' : 'Minimal Changes'}
            </h3>
            <p className="text-sm text-gray-600">
              {formData.restructurePercentage >= 75 ? 'Maximum tax optimization with comprehensive restructuring including advanced entity strategies, aggressive depreciation, and complex planning.' :
               formData.restructurePercentage >= 50 ? 'Moderate restructuring focusing on high-impact strategies with manageable complexity and compliance.' :
               formData.restructurePercentage >= 25 ? 'Simple optimizations using existing structures with minimal operational changes.' :
               'Basic tax planning improvements without significant structural changes.'}
            </p>
          </div>
        </div>

        <div className="flex justify-between mt-8">
          <button
            onClick={prevStep}
            className="px-6 py-3 border border-gray-300 rounded-lg font-medium text-gray-700 hover:bg-gray-50"
          >
            ← Previous
          </button>
          <button
            onClick={nextStep}
            disabled={!formData.restructurePercentage}
            className={`px-8 py-3 rounded-lg font-bold transition-all duration-200 ${
              formData.restructurePercentage
                ? 'bg-emerald-500 hover:bg-emerald-600 text-white'
                : 'bg-gray-300 text-gray-500 cursor-not-allowed'
            }`}
          >
            Continue →
          </button>
        </div>
      </div>
    </div>
  );

  // Step 5: Strategy Goal Selection
  const renderStep5 = () => (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-navy-900 mb-4">
          Step 5: Strategy Goals
        </h1>
        <p className="text-xl text-gray-600">
          What are your primary tax planning objectives?
        </p>
      </div>

      <div className="bg-white rounded-xl shadow-lg p-8">
        <h2 className="text-2xl font-bold text-navy-900 mb-6">Select Your Goals</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
          {[
            {
              id: 'reduce-current-tax',
              title: 'Reduce Current Year Tax',
              description: 'Immediate tax savings for this tax year',
              icon: '💰'
            },
            {
              id: 'build-wealth',
              title: 'Build Long-term Wealth',
              description: 'Compound tax savings into long-term investments',
              icon: '📈'
            },
            {
              id: 'real-estate',
              title: 'Real Estate Investment',
              description: 'Leverage real estate for depreciation and cash flow',
              icon: '🏠'
            },
            {
              id: 'business-optimization',
              title: 'Business Structure Optimization',
              description: 'Optimize entity structure and business deductions',
              icon: '🏢'
            },
            {
              id: 'retirement-planning',
              title: 'Retirement Planning',
              description: 'Maximize retirement contributions and tax deferrals',
              icon: '🎯'
            },
            {
              id: 'estate-planning',
              title: 'Estate & Legacy Planning',
              description: 'Wealth transfer and estate tax minimization',
              icon: '👨‍👩‍👧‍👦'
            }
          ].map((goal) => (
            <div
              key={goal.id}
              onClick={() => handleGoalChange(goal.id)}
              className={`p-4 border-2 rounded-lg cursor-pointer transition-all duration-200 ${
                formData.primaryGoals.includes(goal.id)
                  ? 'border-emerald-500 bg-emerald-50'
                  : 'border-gray-200 hover:border-emerald-300'
              }`}
            >
              <div className="flex items-start">
                <div className="text-2xl mr-4">{goal.icon}</div>
                <div>
                  <h3 className="font-bold text-navy-900 mb-1">{goal.title}</h3>
                  <p className="text-sm text-gray-600">{goal.description}</p>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="border-t pt-6">
          <h3 className="text-lg font-bold text-navy-900 mb-4">Implementation Timeframe</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {[
              {
                value: 'immediate',
                title: 'Immediate (0-6 months)',
                description: 'Need results before year-end'
              },
              {
                value: 'short-term',
                title: 'Short-term (6-18 months)',
                description: 'Planned implementation over next year'
              },
              {
                value: 'long-term',
                title: 'Long-term (1-3 years)',
                description: 'Strategic multi-year planning'
              }
            ].map((option) => (
              <div
                key={option.value}
                onClick={() => setFormData(prev => ({ ...prev, timeframe: option.value }))}
                className={`p-4 border-2 rounded-lg cursor-pointer transition-all duration-200 ${
                  formData.timeframe === option.value
                    ? 'border-emerald-500 bg-emerald-50'
                    : 'border-gray-200 hover:border-emerald-300'
                }`}
              >
                <h4 className="font-bold text-navy-900 mb-1">{option.title}</h4>
                <p className="text-xs text-gray-600">{option.description}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="flex justify-between mt-8">
          <button
            onClick={prevStep}
            className="px-6 py-3 border border-gray-300 rounded-lg font-medium text-gray-700 hover:bg-gray-50"
          >
            ← Previous
          </button>
          <button
            onClick={nextStep}
            disabled={formData.primaryGoals.length === 0}
            className={`px-8 py-3 rounded-lg font-bold transition-all duration-200 ${
              formData.primaryGoals.length > 0
                ? 'bg-emerald-500 hover:bg-emerald-600 text-white'
                : 'bg-gray-300 text-gray-500 cursor-not-allowed'
            }`}
          >
            Continue →
          </button>
        </div>
      </div>
    </div>
  );

  // Step 6: Forecast Settings
  const renderStep6 = () => (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-navy-900 mb-4">
          Step 6: Forecast Settings
        </h1>
        <p className="text-xl text-gray-600">
          Configure your wealth projection parameters
        </p>
      </div>

      <div className="bg-white rounded-xl shadow-lg p-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Forecast Controls */}
          <div>
            <h2 className="text-2xl font-bold text-navy-900 mb-6">Projection Settings</h2>
            
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Forecast Time Horizon: {formData.forecastTimeHorizon} years
                </label>
                <input
                  type="range"
                  name="forecastTimeHorizon"
                  value={formData.forecastTimeHorizon}
                  onChange={handleInputChange}
                  min="5"
                  max="20"
                  step="1"
                  className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                  style={{
                    background: `linear-gradient(to right, #10b981 0%, #10b981 ${((formData.forecastTimeHorizon - 5) / 15) * 100}%, #e5e7eb ${((formData.forecastTimeHorizon - 5) / 15) * 100}%, #e5e7eb 100%)`
                  }}
                />
                <div className="flex justify-between text-xs text-gray-500 mt-1">
                  <span>5 years</span>
                  <span>20 years</span>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Expected Return Rate: {formData.returnRate}%
                </label>
                <input
                  type="range"
                  name="returnRate"
                  value={formData.returnRate}
                  onChange={handleInputChange}
                  min="3"
                  max="12"
                  step="0.5"
                  className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                  style={{
                    background: `linear-gradient(to right, #10b981 0%, #10b981 ${((formData.returnRate - 3) / 9) * 100}%, #e5e7eb ${((formData.returnRate - 3) / 9) * 100}%, #e5e7eb 100%)`
                  }}
                />
                <div className="flex justify-between text-xs text-gray-500 mt-1">
                  <span>3% (Conservative)</span>
                  <span>12% (Aggressive)</span>
                </div>
              </div>

              <div className="bg-emerald-50 border border-emerald-200 rounded-lg p-4">
                <div className="flex items-center">
                  <input
                    type="checkbox"
                    name="reinvestTaxSavings"
                    checked={formData.reinvestTaxSavings}
                    onChange={handleInputChange}
                    className="h-4 w-4 text-emerald-600 focus:ring-emerald-500 border-gray-300 rounded"
                  />
                  <label className="ml-3 font-medium text-emerald-800">
                    Enable Wealth Multiplier Loop
                    <span className="block text-sm text-emerald-600 font-normal">
                      Automatically reinvest tax savings for compounding growth
                    </span>
                  </label>
                </div>
              </div>
            </div>
          </div>

          {/* Preview Calculations */}
          <div>
            <h2 className="text-2xl font-bold text-navy-900 mb-6">Quick Preview</h2>
            
            <div className="bg-gray-50 rounded-lg p-6">
              <div className="space-y-4">
                <div className="flex justify-between">
                  <span className="text-gray-600">Annual Income:</span>
                  <span className="font-bold text-navy-900">${formData.annualIncome}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Capital Available:</span>
                  <span className="font-bold text-navy-900">${formData.capitalToAllocate}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Restructure %:</span>
                  <span className="font-bold text-navy-900">{formData.restructurePercentage}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Time Horizon:</span>
                  <span className="font-bold text-navy-900">{formData.forecastTimeHorizon} years</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Return Rate:</span>
                  <span className="font-bold text-navy-900">{formData.returnRate}%</span>
                </div>
                <div className="border-t pt-4">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Selected Goals:</span>
                    <span className="font-bold text-navy-900">{formData.primaryGoals.length}</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <h3 className="font-bold text-blue-900 mb-2">💡 Forecast Assumptions</h3>
              <ul className="text-sm text-blue-800 space-y-1">
                <li>• Tax savings reinvested annually</li>
                <li>• Returns compound over time horizon</li>
                <li>• Strategies implemented gradually</li>
                <li>• Tax rates remain relatively stable</li>
              </ul>
            </div>
          </div>
        </div>

        <div className="flex justify-between mt-8">
          <button
            onClick={prevStep}
            className="px-6 py-3 border border-gray-300 rounded-lg font-medium text-gray-700 hover:bg-gray-50"
          >
            ← Previous
          </button>
          <button
            onClick={nextStep}
            className="px-8 py-3 bg-emerald-500 hover:bg-emerald-600 text-white rounded-lg font-bold transition-all duration-200"
          >
            Continue →
          </button>
        </div>
      </div>
    </div>
  );

  // Step 7: Entity Review  
  const renderStep7 = () => (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-navy-900 mb-4">
          Step 7: Entity Review
        </h1>
        <p className="text-xl text-gray-600">
          Review and optimize your current business structure
        </p>
      </div>

      <div className="bg-white rounded-xl shadow-lg p-8">
        <h2 className="text-2xl font-bold text-navy-900 mb-6">Current Entity Structure</h2>
        
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Current Business Structure
            </label>
            <select
              name="currentEntityStructure"
              value={formData.currentEntityStructure}
              onChange={handleInputChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
            >
              <option value="">Select current structure</option>
              <option value="sole-proprietorship">Sole Proprietorship</option>
              <option value="single-llc">Single-Member LLC</option>
              <option value="multi-llc">Multi-Member LLC</option>
              <option value="partnership">Partnership</option>
              <option value="s-corp">S-Corporation</option>
              <option value="c-corp">C-Corporation</option>
              <option value="none">No formal structure</option>
              <option value="other">Other</option>
            </select>
          </div>

          {/* Entity Analysis */}
          {formData.currentEntityStructure && (
            <div className="mt-8 p-6 bg-blue-50 border border-blue-200 rounded-lg">
              <h3 className="text-lg font-bold text-navy-900 mb-4">Entity Analysis</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h4 className="font-semibold text-gray-900 mb-2">Current Benefits</h4>
                  <ul className="text-sm text-gray-700 space-y-1">
                    {formData.currentEntityStructure === 'sole-proprietorship' && (
                      <>
                        <li>✓ Simple tax filing</li>
                        <li>✓ Full business control</li>
                        <li>✗ Personal liability exposure</li>
                        <li>✗ Self-employment tax on all income</li>
                      </>
                    )}
                    {formData.currentEntityStructure === 's-corp' && (
                      <>
                        <li>✓ Payroll tax savings potential</li>
                        <li>✓ Pass-through taxation</li>
                        <li>✗ Reasonable salary requirements</li>
                        <li>✗ Limited ownership structure</li>
                      </>
                    )}
                    {formData.currentEntityStructure === 'c-corp' && (
                      <>
                        <li>✓ Lower corporate tax rates</li>
                        <li>✓ Retained earnings benefits</li>
                        <li>✗ Double taxation potential</li>
                        <li>✗ Complex compliance requirements</li>
                      </>
                    )}
                  </ul>
                </div>
                
                <div>
                  <h4 className="font-semibold text-gray-900 mb-2">Optimization Opportunities</h4>
                  <ul className="text-sm text-emerald-700 space-y-1">
                    {formData.currentEntityStructure === 'sole-proprietorship' && (
                      <>
                        <li>• Consider LLC for liability protection</li>
                        <li>• S-Corp election for tax savings</li>
                        <li>• Business expense optimization</li>
                      </>
                    )}
                    {formData.currentEntityStructure === 's-corp' && parseFormattedNumber(formData.annualIncome) > 500000 && (
                      <>
                        <li>• C-Corp MSO structure evaluation</li>
                        <li>• Advanced deduction strategies</li>
                        <li>• Retained earnings planning</li>
                      </>
                    )}
                  </ul>
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="flex justify-between mt-8">
          <button
            onClick={prevStep}
            className="px-6 py-3 border border-gray-300 rounded-lg font-medium text-gray-700 hover:bg-gray-50"
          >
            ← Previous
          </button>
          <button
            onClick={nextStep}
            disabled={!formData.currentEntityStructure}
            className={`px-8 py-3 rounded-lg font-bold transition-all duration-200 ${
              formData.currentEntityStructure
                ? 'bg-emerald-500 hover:bg-emerald-600 text-white'
                : 'bg-gray-300 text-gray-500 cursor-not-allowed'
            }`}
          >
            Continue →
          </button>
        </div>
      </div>
    </div>
  );

  // Step 8: Financial Summary
  const renderStep8 = () => {
    // Calculate financial summary
    const annualIncome = parseFormattedNumber(formData.annualIncome);
    const capitalAvailable = parseFormattedNumber(formData.capitalToAllocate);
    const stockCompValue = parseFormattedNumber(formData.stockCompValue);
    
    const estimatedCurrentTax = annualIncome * 0.25; // Rough estimate
    const potentialSavings = Math.min(estimatedCurrentTax * 0.4, capitalAvailable * 0.8);
    
    return (
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-navy-900 mb-4">
            Step 8: Financial Summary
          </h1>
          <p className="text-xl text-gray-600">
            Review your financial profile and projected opportunities
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Current Financial Profile */}
          <div className="bg-white rounded-xl shadow-lg p-8">
            <h2 className="text-2xl font-bold text-navy-900 mb-6">Current Financial Profile</h2>
            
            <div className="space-y-4">
              <div className="flex justify-between items-center py-3 border-b border-gray-200">
                <span className="text-gray-600">Income Type:</span>
                <span className="font-semibold text-navy-900 capitalize">
                  {formData.incomeType === 'w2' ? 'W-2 Employee' : 
                   formData.incomeType === 'mixed' ? 'Mixed Income' : 'Business Owner'}
                </span>
              </div>
              
              <div className="flex justify-between items-center py-3 border-b border-gray-200">
                <span className="text-gray-600">Annual Income:</span>
                <span className="font-semibold text-navy-900">${formData.annualIncome}</span>
              </div>
              
              <div className="flex justify-between items-center py-3 border-b border-gray-200">
                <span className="text-gray-600">Capital Available:</span>
                <span className="font-semibold text-navy-900">${formData.capitalToAllocate}</span>
              </div>
              
              {formData.hasStockCompensation && (
                <div className="flex justify-between items-center py-3 border-b border-gray-200">
                  <span className="text-gray-600">Stock Compensation:</span>
                  <span className="font-semibold text-navy-900">${formData.stockCompValue}</span>
                </div>
              )}
              
              <div className="flex justify-between items-center py-3 border-b border-gray-200">
                <span className="text-gray-600">Restructure Percentage:</span>
                <span className="font-semibold text-navy-900">{formData.restructurePercentage}%</span>
              </div>
              
              <div className="flex justify-between items-center py-3">
                <span className="text-gray-600">Entity Structure:</span>
                <span className="font-semibold text-navy-900 capitalize">
                  {formData.currentEntityStructure?.replace('-', ' ') || 'None'}
                </span>
              </div>
            </div>
          </div>

          {/* Projected Opportunities */}
          <div className="bg-gradient-to-br from-emerald-50 to-emerald-100 border border-emerald-200 rounded-xl p-8">
            <h2 className="text-2xl font-bold text-emerald-900 mb-6">Projected Opportunities</h2>
            
            <div className="space-y-6">
              <div className="bg-white rounded-lg p-4">
                <div className="text-center">
                  <div className="text-3xl font-bold text-emerald-600 mb-2">
                    ${potentialSavings.toLocaleString()}
                  </div>
                  <div className="text-sm text-gray-600">Estimated Annual Tax Savings</div>
                </div>
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-white rounded-lg p-4 text-center">
                  <div className="text-xl font-bold text-navy-900">{formData.forecastTimeHorizon}</div>
                  <div className="text-xs text-gray-600">Year Projection</div>
                </div>
                <div className="bg-white rounded-lg p-4 text-center">
                  <div className="text-xl font-bold text-navy-900">{formData.returnRate}%</div>
                  <div className="text-xs text-gray-600">Expected Return</div>
                </div>
              </div>
              
              <div className="bg-white rounded-lg p-4">
                <h3 className="font-bold text-gray-900 mb-2">Strategy Alignment</h3>
                <div className="space-y-2">
                  {formData.primaryGoals.slice(0, 3).map((goal, index) => (
                    <div key={index} className="flex items-center text-sm">
                      <div className="w-2 h-2 bg-emerald-500 rounded-full mr-2"></div>
                      <span className="text-gray-700 capitalize">{goal.replace('-', ' ')}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="flex justify-between mt-8">
          <button
            onClick={prevStep}
            className="px-6 py-3 border border-gray-300 rounded-lg font-medium text-gray-700 hover:bg-gray-50"
          >
            ← Previous
          </button>
          <button
            onClick={nextStep}
            className="px-8 py-3 bg-emerald-500 hover:bg-emerald-600 text-white rounded-lg font-bold transition-all duration-200"
          >
            Generate Strategy Recommendations →
          </button>
        </div>
      </div>
    );
  };

  // Step 9: Strategy Recommendations
  const renderStep9 = () => {
    // Generate strategies based on user profile
    const generatedStrategies = generateStrategies();
    
    return (
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-navy-900 mb-4">
            Step 9: Your Personalized Strategy Recommendations
          </h1>
          <p className="text-xl text-gray-600">
            Complete implementation roadmap with wealth projections
          </p>
        </div>

        {/* Wealth Multiplier Loop Visualization */}
        <div className="bg-gradient-to-r from-emerald-500 to-emerald-600 rounded-xl p-8 text-white mb-8">
          <h2 className="text-3xl font-bold text-center mb-8">Wealth Multiplier Loop</h2>
          
          <div className="flex items-center justify-between max-w-4xl mx-auto">
            <div className="text-center">
              <div className="w-24 h-24 bg-white text-emerald-600 rounded-full flex items-center justify-center font-bold text-lg mb-4">
                Step 1
              </div>
              <div className="text-emerald-100">Tax Savings</div>
              <div className="text-2xl font-bold">${(parseFormattedNumber(formData.annualIncome) * 0.1).toLocaleString()}</div>
            </div>
            
            <div className="text-4xl">→</div>
            
            <div className="text-center">
              <div className="w-24 h-24 bg-white text-emerald-600 rounded-full flex items-center justify-center font-bold text-lg mb-4">
                Step 2
              </div>
              <div className="text-emerald-100">Reinvestment</div>
              <div className="text-2xl font-bold">{formData.returnRate}% Return</div>
            </div>
            
            <div className="text-4xl">→</div>
            
            <div className="text-center">
              <div className="w-24 h-24 bg-white text-emerald-600 rounded-full flex items-center justify-center font-bold text-lg mb-4">
                Step 3
              </div>
              <div className="text-emerald-100">Compounding</div>
              <div className="text-2xl font-bold">{formData.forecastTimeHorizon} Years</div>
            </div>
            
            <div className="text-4xl">→</div>
            
            <div className="text-center">
              <div className="w-24 h-24 bg-white text-emerald-600 rounded-full flex items-center justify-center font-bold text-lg mb-4">
                Result
              </div>
              <div className="text-emerald-100">Future Value</div>
              <div className="text-2xl font-bold">
                ${(parseFormattedNumber(formData.annualIncome) * 0.1 * Math.pow(1 + formData.returnRate / 100, formData.forecastTimeHorizon)).toLocaleString()}
              </div>
            </div>
          </div>
          
          <div className="text-center mt-8">
            <button className="bg-white text-emerald-600 px-4 py-2 rounded-lg font-medium hover:bg-gray-100 inline-flex items-center">
              <span className="mr-2">ℹ️</span>
              View Detailed Assumptions
            </button>
          </div>
        </div>

        {/* Strategy Stack */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
          {Object.entries(generatedStrategies).map(([category, categoryStrategies]) => (
            <div key={category} className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="text-xl font-bold text-navy-900 mb-4 capitalize">
                {category === 'setup' ? 'Setup & Structure' : 
                 category === 'deductions' ? 'Deduction Strategies' : 'Exit Planning'}
              </h3>
              
              <div className="space-y-4">
                {categoryStrategies.map((strategy, index) => (
                  <div key={index} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex justify-between items-start mb-2">
                      <h4 className="font-semibold text-gray-900">{strategy.title}</h4>
                      <span className={`px-2 py-1 rounded text-xs ${
                        strategy.complexity === 'Beginner' ? 'bg-green-100 text-green-600' :
                        strategy.complexity === 'Intermediate' ? 'bg-yellow-100 text-yellow-600' :
                        'bg-red-100 text-red-600'
                      }`}>
                        {strategy.complexity}
                      </span>
                    </div>
                    
                    <p className="text-sm text-gray-600 mb-3">{strategy.description}</p>
                    
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-xs text-gray-500">Implementation Status</span>
                      <select
                        value={implementationStatus[strategy.id] || 'not-started'}
                        onChange={(e) => handleStrategyStatusChange(strategy.id, e.target.value)}
                        className="text-xs border border-gray-300 rounded px-2 py-1"
                      >
                        <option value="not-started">Not Started</option>
                        <option value="in-progress">In Progress</option>
                        <option value="complete">Complete</option>
                      </select>
                    </div>
                    
                    <div className="text-xs text-emerald-600 font-medium">
                      Max Savings: ${strategy.maxSavings?.toLocaleString()}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* Implementation Tracker */}
        <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
          <h2 className="text-2xl font-bold text-navy-900 mb-6">Implementation Tracker</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
            <div className="text-center">
              <div className="text-3xl font-bold text-emerald-600">
                {Object.values(implementationStatus).filter(status => status === 'complete').length}
              </div>
              <div className="text-gray-600">Strategies Complete</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-yellow-600">
                {Object.values(implementationStatus).filter(status => status === 'in-progress').length}
              </div>
              <div className="text-gray-600">In Progress</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-gray-600">
                {Object.values(implementationStatus).filter(status => status === 'not-started').length}
              </div>
              <div className="text-gray-600">Not Started</div>
            </div>
          </div>
          
          <div className="w-full bg-gray-200 rounded-full h-4 mb-4">
            <div 
              className="bg-emerald-500 h-4 rounded-full transition-all duration-500"
              style={{ 
                width: `${Object.values(implementationStatus).length > 0 ? 
                  (Object.values(implementationStatus).filter(status => status === 'complete').length / 
                   Object.values(implementationStatus).length) * 100 : 0}%` 
              }}
            ></div>
          </div>
          
          <div className="text-center text-gray-600">
            {Object.values(implementationStatus).length > 0 ? 
              Math.round((Object.values(implementationStatus).filter(status => status === 'complete').length / 
                         Object.values(implementationStatus).length) * 100) : 0}% Complete
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex justify-between">
          <button
            onClick={prevStep}
            className="px-6 py-3 border border-gray-300 rounded-lg font-medium text-gray-700 hover:bg-gray-50"
          >
            ← Previous
          </button>
          <div className="space-x-4">
            <button
              onClick={() => setCurrentStep(1)}
              className="px-6 py-3 border border-emerald-500 text-emerald-600 rounded-lg font-medium hover:bg-emerald-50"
            >
              Start Over
            </button>
            <button
              onClick={() => alert('Your escape plan has been saved! Implementation guidance will be sent to your email.')}
              className="px-8 py-3 bg-emerald-500 hover:bg-emerald-600 text-white rounded-lg font-bold"
            >
              Save My Escape Plan
            </button>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-6 py-12">
        {renderStepProgress()}
        {currentStep === 1 && renderStep1()}
        {currentStep === 2 && renderStep2()}
        {currentStep === 3 && renderStep3()}
        {currentStep === 4 && renderStep4()}
        {currentStep === 5 && renderStep5()}
        {currentStep === 6 && renderStep6()}
        {currentStep === 7 && renderStep7()}
        {currentStep === 8 && renderStep8()}
        {currentStep === 9 && renderStep9()}
      </div>
    </div>
  );
};

export default BuildEscapePlan;