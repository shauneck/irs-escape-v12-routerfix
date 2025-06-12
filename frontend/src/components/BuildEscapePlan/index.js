import React, { useState, useEffect } from 'react';

const BuildEscapePlan = () => {
  const [formData, setFormData] = useState({
    income: '',
    incomeType: 'w2',
    currentTaxRate: '',
    goals: [],
    timeframe: '1-year'
  });

  const [plan, setPlan] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleGoalChange = (goal) => {
    setFormData(prev => ({
      ...prev,
      goals: prev.goals.includes(goal) 
        ? prev.goals.filter(g => g !== goal)
        : [...prev.goals, goal]
    }));
  };

  const generatePlan = async () => {
    setLoading(true);
    
    // Simulate API call - this would integrate with a real tax planning service
    setTimeout(() => {
      const mockPlan = {
        projectedSavings: Math.floor(parseFloat(formData.income) * 0.15),
        strategies: [
          'Real Estate Professional Status (REPS) Qualification',
          'Strategic Deduction Portfolio',
          'Tax-Advantaged Investment Repositioning',
          'Entity Structure Optimization'
        ],
        timeline: formData.timeframe,
        nextSteps: [
          'Complete detailed income analysis',
          'Evaluate REPS qualification potential',
          'Implement strategic deduction framework',
          'Monitor and optimize quarterly'
        ]
      };
      setPlan(mockPlan);
      setLoading(false);
    }, 2000);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-6 py-12">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="text-center mb-12">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              Build Your Escape Plan
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Create your personalized tax plan with optimized strategies and lifetime projections.
              Get a comprehensive roadmap to legally minimize your tax burden while building wealth.
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            {/* Form Section */}
            <div className="bg-white rounded-lg shadow-lg p-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Tell Us About Your Situation</h2>
              
              <div className="space-y-6">
                {/* Income Input */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Annual Income
                  </label>
                  <input
                    type="number"
                    name="income"
                    value={formData.income}
                    onChange={handleInputChange}
                    placeholder="Enter your annual income"
                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  />
                </div>

                {/* Income Type */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Primary Income Type
                  </label>
                  <select
                    name="incomeType"
                    value={formData.incomeType}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  >
                    <option value="w2">W-2 Employee</option>
                    <option value="business">Business Owner</option>
                    <option value="self-employed">Self-Employed</option>
                    <option value="investor">Investor</option>
                    <option value="mixed">Mixed Sources</option>
                  </select>
                </div>

                {/* Current Tax Rate */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Current Effective Tax Rate (%)
                  </label>
                  <input
                    type="number"
                    name="currentTaxRate"
                    value={formData.currentTaxRate}
                    onChange={handleInputChange}
                    placeholder="e.g., 25"
                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  />
                </div>

                {/* Goals */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-3">
                    Tax Planning Goals (Select all that apply)
                  </label>
                  <div className="space-y-2">
                    {[
                      'Reduce current year tax liability',
                      'Build long-term wealth',
                      'Real estate investment strategy',
                      'Business structure optimization',
                      'Retirement planning',
                      'Estate planning'
                    ].map(goal => (
                      <label key={goal} className="flex items-center">
                        <input
                          type="checkbox"
                          checked={formData.goals.includes(goal)}
                          onChange={() => handleGoalChange(goal)}
                          className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
                        />
                        <span className="ml-2 text-sm text-gray-700">{goal}</span>
                      </label>
                    ))}
                  </div>
                </div>

                {/* Timeframe */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Planning Timeframe
                  </label>
                  <select
                    name="timeframe"
                    value={formData.timeframe}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  >
                    <option value="immediate">Immediate (this year)</option>
                    <option value="1-year">1-3 years</option>
                    <option value="5-year">5-10 years</option>
                    <option value="long-term">10+ years</option>
                  </select>
                </div>

                {/* Generate Button */}
                <button
                  onClick={generatePlan}
                  disabled={!formData.income || loading}
                  className="w-full bg-green-600 text-white py-3 px-6 rounded-md font-semibold hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
                >
                  {loading ? 'Generating Your Plan...' : 'Generate Escape Plan'}
                </button>
              </div>
            </div>

            {/* Results Section */}
            <div className="bg-white rounded-lg shadow-lg p-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Your Personalized Plan</h2>
              
              {!plan && !loading && (
                <div className="text-center py-12">
                  <div className="text-gray-400 mb-4">
                    <svg className="mx-auto h-24 w-24" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                  <p className="text-gray-500">Complete the form to generate your personalized tax escape plan</p>
                </div>
              )}

              {loading && (
                <div className="text-center py-12">
                  <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600 mx-auto mb-4"></div>
                  <p className="text-gray-600">Analyzing your situation and generating strategies...</p>
                </div>
              )}

              {plan && (
                <div className="space-y-6">
                  {/* Projected Savings */}
                  <div className="bg-green-50 border border-green-200 rounded-lg p-6">
                    <h3 className="text-lg font-semibold text-green-800 mb-2">Projected Annual Savings</h3>
                    <p className="text-3xl font-bold text-green-600">${plan.projectedSavings?.toLocaleString()}</p>
                    <p className="text-sm text-green-700 mt-1">Based on optimized tax strategies</p>
                  </div>

                  {/* Recommended Strategies */}
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-3">Recommended Strategies</h3>
                    <ul className="space-y-2">
                      {plan.strategies?.map((strategy, index) => (
                        <li key={index} className="flex items-start">
                          <svg className="h-5 w-5 text-green-500 mt-0.5 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                          </svg>
                          <span className="text-gray-700">{strategy}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* Next Steps */}
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-3">Next Steps</h3>
                    <ol className="space-y-2">
                      {plan.nextSteps?.map((step, index) => (
                        <li key={index} className="flex items-start">
                          <span className="flex-shrink-0 h-6 w-6 bg-green-100 text-green-800 rounded-full flex items-center justify-center text-sm font-medium mr-3">
                            {index + 1}
                          </span>
                          <span className="text-gray-700">{step}</span>
                        </li>
                      ))}
                    </ol>
                  </div>

                  {/* Call to Action */}
                  <div className="bg-gray-50 border border-gray-200 rounded-lg p-6">
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">Ready to Implement?</h3>
                    <p className="text-gray-600 mb-4">
                      Work with our tax strategists to implement your personalized escape plan and start saving immediately.
                    </p>
                    <button className="bg-green-600 text-white py-2 px-6 rounded-md font-semibold hover:bg-green-700 transition-colors">
                      Schedule Strategy Call
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Features Section */}
          <div className="mt-16">
            <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
              Why Choose Our Escape Plan Builder?
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="h-8 w-8 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">Data-Driven Analysis</h3>
                <p className="text-gray-600">Advanced algorithms analyze your financial situation to identify maximum tax savings opportunities.</p>
              </div>
              <div className="text-center">
                <div className="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="h-8 w-8 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">Actionable Strategies</h3>
                <p className="text-gray-600">Get specific, implementable tax strategies tailored to your income type and financial goals.</p>
              </div>
              <div className="text-center">
                <div className="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="h-8 w-8 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">Lifetime Projections</h3>
                <p className="text-gray-600">See long-term impact of your tax strategies with comprehensive wealth-building projections.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BuildEscapePlan;