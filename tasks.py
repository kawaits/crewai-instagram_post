from crewai import Task
from textwrap import dedent

class MarketingAnalysisTasks:
	def product_analysis(self, agent, product_website, product_details):
		return Task(
			description=dedent(f"""\
			Analyze the given product website: {product_website}.
			Extra details provided by the customer: {product_details}.

			Focus on identifying unique features, benefits,
			and the overall narrative presented.

			Your final report should clearly articulate the
			product's key selling points, its market appeal,
			and suggestions for enhancement or positioning.
			Emphasize the aspects that make the product stand out.

			Keep in mind, attention to detail is crucial for
			a comprehensive analysis. It's currenlty 2024.
			"""),
			expected_output=dedent("""\
				A structured product analysis report including:
				- Key features and benefits
				- Target audience and positioning
				- Differentiators vs typical alternatives
				- Actionable suggestions for messaging and positioning
			"""),
			agent=agent,
		)

	def competitor_analysis(self, agent, product_website, product_details):
		return Task(
			description=dedent(f"""\
			Explore competitor of: {product_website}.
			Extra details provided by the customer: {product_details}.

			Identify the top 3 competitors and analyze their
			strategies, market positioning, and customer perception.

			Your final report MUST include BOTH all context about {product_website}
			and a detailed comparison to whatever competitor they have competitors.
			"""),
			expected_output=dedent(f"""\
				A competitor analysis report that includes:
				- The top 3 competitors (with links/names)
				- For each competitor: positioning, messaging, offers, and audience
				- A comparison section vs {product_website}
				- Key opportunities for differentiation
			"""),
			agent=agent,
		)

	def campaign_development(self, agent, product_website, product_details):
		return Task(
			description=dedent(f"""\
			You're creating a targeted marketing campaign for: {product_website}.
			Extra details provided by the customer: {product_details}.

			To start this campaing we will need a strategy and creative content ideas.
			It should be meticulously designed to captivate and engage
			the product's target audience.

			Based on your ideas your co-workers will create the content for the campaign.

			Your final answer MUST be ideas that will resonate with the audience and
			also include ALL context you have about the product and the customer.
			"""),
			expected_output=dedent("""\
				A campaign strategy outline including:
				- Campaign goal and target audience
				- Core message and creative direction
				- 3-5 content ideas (hooks/angles)
				- Suggested CTAs and posting approach
			"""),
			agent=agent,
		)

	def instagram_ad_copy(self, agent):
		return Task(
			description=dedent("""\
			Craft an engaging Instagram post copy.
			The copy should be punchy, captivating, concise,
			and aligned with the product marketing strategy.

			Focus on creating a message that resonates with
			the target audience and highlights the product's
			unique selling points.

			Your ad copy must be attention-grabbing and should
			encourage viewers to take action, whether it's
			visiting the website, making a purchase, or learning
			more about the product.

			Your final answer MUST be 3 options for an ad copy for instagram that
			not only informs but also excites and persuades the audience.
			"""),
			expected_output=dedent("""\
				Exactly 3 distinct Instagram caption options, each including:
				- A strong hook in the first line
				- 1-3 short paragraphs or lines (mobile-friendly)
				- A clear call to action
				Optionally: relevant hashtags (kept minimal).
			"""),
			agent=agent,
		)

	def take_photograph_task(self, agent, copy, product_website, product_details):
		return Task(
			description=dedent(f"""\
			You are working on a new campaign for a super important customer,
			and you MUST take the most amazing photo ever for an instagram post
			regarding the product, you have the following copy:
			{copy}

			This is the product you are working with: {product_website}.
			Extra details provided by the customer: {product_details}.

			Imagine what the photo you wanna take describe it in a paragraph.
			Here are some examples for you follow:
			- high tech airplaine in a beautiful blue sky in a beautiful sunset super cripsy beautiful 4k, professional wide shot
			- the last supper, with Jesus and his disciples, breaking bread, close shot, soft lighting, 4k, crisp
			- an bearded old man in the snows, using very warm clothing, with mountains full of snow behind him, soft lighting, 4k, crisp, close up to the camera

			Think creatively and focus on how the image can capture the audience's
			attention. Don't show the actual product on the photo.

			Your final answer must be 3 options of photographs, each with 1 paragraph
			describing the photograph exactly like the examples provided above.
			"""),
			expected_output=dedent("""\
				Exactly 3 distinct photo prompt descriptions.
				Each option must be a single paragraph in the same style as the examples
				(highly visual, includes shot type/lighting/quality keywords).
			"""),
			agent=agent,
		)

	def review_photo(self, agent, product_website, product_details):
		return Task(
			description=dedent(f"""\
			Review the photos you got from the senior photographer.
			Make sure it's the best possible and aligned with the product's goals,
			review, approve, ask clarifying question or delegate follow up work if
			necessary to make decisions. When delegating work send the full draft
			as part of the information.

			This is the product you are working with: {product_website}.
			Extra details provided by the customer: {product_details}.

			Here are some examples on how the final photographs should look like:
			- high tech airplaine in a beautiful blue sky in a beautiful sunset super cripsy beautiful 4k, professional wide shot
			- the last supper, with Jesus and his disciples, breaking bread, close shot, soft lighting, 4k, crisp
			- an bearded old man in the snows, using very warm clothing, with mountains full of snow behind him, soft lighting, 4k, crisp, close up to the camera

			Your final answer must be 3 reviewed options of photographs,
			each with 1 paragraph description following the examples provided above.
			"""),
			expected_output=dedent("""\
				Exactly 3 reviewed/refined photo descriptions, each:
				- One paragraph
				- Polished for clarity and impact
				- Aligned with the product and campaign goals
			"""),
			agent=agent,
		)