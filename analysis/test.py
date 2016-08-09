# Old way od doing legend
# ------ legend left/right ------------

# _legends = {}
# _legends['_left'] = ROOT.TLegend(0.45, 0.6,0.75,0.92)
# _legends['_right']= ROOT.TLegend(0.68, 0.6,0.92,0.92)

# # data stack histogram has only one legend entry
# _legends['_left'].AddEntry( _stack_histograms[_data], 'Data', 'p')
# # mc stack histograms have their own legend entries
# for _i, _s in enumerate(_samples):
# 	if self.all_samples[_s]['types'] == 'mc':
# 		# left/right legend
# 		if _i%2 != 0:
# 			_legends['_left'].AddEntry(_histograms[_v + '-' + _s],'test','f')
# 		else:
# 			_legends['_right'].AddEntry(_histograms[_v + '-' + _s], 'test', 'f')

# # both legends have the same options
# for _l in _legends.keys():
# 	_legends[_l].SetLineWidth(2)
# 	_legends[_l].SetBorderSize(1)
# 	_legends[_l].SetFillColor(0)
# 	_legends[_l].SetFillStyle(4000)
# 	_legends[_l].SetTextFont(62)
# 	_legends[_l].SetTextSize(0.035)
# 	_legends[_l].Draw()
# _legends['_right'].AddEntry(_error_graph,"MC uncert. (stat.)","fl")


		# # Add data to legend first
		# for _s in self.samples_plot.values():
		# 	# constraint of marker size just to add one data histogram in legend
		# 	_sample_type = self.samples_all[_s]['types']
		# 	_marker_size = self.histograms[variable+'-'+_s].GetMarkerSize()
		# 	if _sample_type == 'data' and _marker_size > 0.01:
		# 		self.legends['stack_legend'].AddEntry( self.histograms[variable + '-' + _s], 'Data', 'p')

		# # Add mc to legend for each sample
		# for _s in self.samples_plot.values():
		# 	_sample_type = self.samples_all[_s]['types']
		# 	if _sample_type == 'mc':
		# 		self.legends['stack_legend'].AddEntry( self.histograms[variable + '-' + _s],'test','f')